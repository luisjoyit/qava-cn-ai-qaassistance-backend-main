# src/adapters/user_story_validation_adapter.py
import uuid
import datetime
import logging
from src.ports.test_cases_ports.process_user_story_port import ProcessUserStoryPort
from src.ports.output_ports.llm_port import LLMPort
from src.ports.output_ports.mongo_port import MongoDBPort
from src.ports.test_cases_ports.test_case_prompt_generator_port import TestCasePromptGeneratorPort
from src.ports.conversation_ports.conversation_management_port import ConversationManagementPort
from src.ports.test_cases_ports.count_tokens_port import CountTokensPort

class ProcessUserStoryAdapter(ProcessUserStoryPort):
    def __init__(self, llm: LLMPort, mongo_repo: MongoDBPort, prompt_generator: TestCasePromptGeneratorPort, conversation_manager: ConversationManagementPort, count_tokens: CountTokensPort):
        self.llm = llm
        self.mongo_repo = mongo_repo
        self.conversation_manager = conversation_manager
        self.prompt_generator = prompt_generator
        self.count_tokens = count_tokens
        self.conversation_history = {}
        self.logger = logging.getLogger(__name__)

    def _process_user_story(self, input_data):
        """Procesa una historia de usuario y genera casos de prueba."""
        self.logger.info(f"Procesando historia de usuario con input_data: {input_data}")
        
        # Extraer datos necesarios del input
        conversation_id = input_data['data'].get('conversation_id')
        date_created = input_data['data'].get('created')
        messages = input_data['data'].get('message', [])
        name_history = input_data['data'].get('nameHistory')
        step = input_data['data'].get('step')
        user_id = input_data['data'].get('userID')
        testType = input_data['data'].get('testType')
        typeContext = input_data['data'].get('typeContext')
        max_tokens = 3500
        
        # Obtener la último conversacion (historia de usuario)
        user_story = messages[-1]['content'] if messages else ""
        
        # Validar la historia de usuario
        is_valid_user_story = self.validate_user_story(user_story)
        self.logger.debug(f"Validez de la historia de usuario: {is_valid_user_story}")

        # Crear nuevas conversacions basados en el input
        new_messages = [
            {
                "id": str(uuid.uuid4()),
                "role": msg['role'],
                "content": msg['content']
            } for msg in messages
        ]
        self.logger.debug(f"Nuevos conversacions creados: {new_messages}")
        
        # Calcular tokens de entrada (user), salida (assistant) y total
        tokens_input = sum(
            self.count_tokens.count_tokens(msg['content'])
            for msg in new_messages
            if msg['role'] == 'user'
        )
        tokens_output = sum(
            self.count_tokens.count_tokens(msg['content'])
            for msg in new_messages
            if msg['role'] == 'assistant'
        )
        total_tokens = tokens_input + tokens_output
        self.logger.debug(f"Tokens de entrada: {tokens_input}, Tokens de salida: {tokens_output}, Total tokens: {total_tokens}")
        
        # Crear conversacions de validación
        validation_messages = []

        if is_valid_user_story:
            # Generar casos de prueba si la historia es válida
            test_cases = self.prompt_generator.promt_generate_test_cases(messages[-2]['content'], user_story)
            validation_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": (
                        f"¡Gracias por la información! A continuación, te presento el caso de prueba generado basado en la Historia de Usuario proporcionada: {test_cases}"
                    ),
                    "validate": True
                }
            ]
        else:
            validation_messages = [
                {
                    "id": str(uuid.uuid4()),
                    "role": "assistant",
                    "content": (
                        "¡Gracias por tu respuesta! Sin embargo, la información proporcionada no parece seguir el formato de una Historia de Usuario. "
                        "Para crear un caso de prueba adecuado, la historia de usuario debe ser clara, concisa y describir lo que un usuario necesita hacer.\n\n"
                        
                        "Asegúrate de que incluya:\n"
                        "  - Un rol claro (quién está solicitando la historia).\n"
                        "  - Una acción específica (qué quiere hacer el usuario).\n"
                        "  - Un resultado deseado (por qué es importante).\n\n"

                        "Por ejemplo, una HU válida sería: \"Como gerente de ventas, quiero enviar el reporte de ventas por correo "
                        "para que el equipo de ventas tenga acceso a información actualizada y pueda tomar decisiones informadas.\""
                    ),
                    "validate": False
                }
            ]

        # Combinar todos los conversacions
        updated_messages = new_messages + validation_messages
        self.logger.debug(f"conversacions actualizados: {updated_messages}")

        # Actualizar tokens de salida y total incluyendo el mensaje de validación
        validation_tokens = sum(self.count_tokens.count_tokens(msg['content']) for msg in validation_messages)
        tokens_output += validation_tokens
        total_tokens += validation_tokens

        # Construir la respuesta
        response_data = {
            "_id": conversation_id,
            "created": date_created,
            "conversation_id": conversation_id,
            "nameHistory": name_history,
            "step": step,
            "typeContext": typeContext,
            "testType": testType,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "tokens": total_tokens,
            "max_tokens": max_tokens,
            "message": updated_messages
        }

        # Preparar documento para MongoDB
        message_to_save = {
            "_id": conversation_id,
            "data": {
                "conversationId": conversation_id,
                "nameHistory": name_history,
                "userId": user_id,
                "typeContext": typeContext,
                "testType": testType,
                "step": step,
                "tokens_input": tokens_input,
                "tokens_output": tokens_output,
                "tokens": total_tokens,
                "max_tokens": max_tokens,
                "message": [
                    msg for msg in updated_messages 
                    if msg['role'] in ["user", "assistant", "system"]
                ]
            }
        }
        
        # Solo actualizar los campos que deseas, excluyendo nameHistory
        update_fields = {
            "data.typeContext": typeContext,
            "data.testType": testType,
            "data.step": step,
            "data.tokens_input": tokens_input,
            "data.tokens_output": tokens_output,
            "data.tokens": total_tokens,
            "data.message": [
                msg for msg in updated_messages 
                if msg['role'] in ["user", "assistant", "system"]
            ]
        }
        self.mongo_repo.update_conversation_user_story(conversation_id, update_fields)
        
        # Guardar en el historial de conversaciones
        self.conversation_history[conversation_id] = updated_messages
        self.conversation_manager.save_conversation(conversation_id, user_story, name_history, is_valid_user_story)
        
        self.logger.info("Procesamiento de historia de usuario completado exitosamente.")
        
        return {"data": response_data}, 200
    
    def validate_user_story(self, user_story: str) -> bool:
        self.logger.debug(f"Validando historia de usuario: {user_story}")
        
        # Generar el prompt para la validación
        validation_prompt = self.prompt_validation_user_story(user_story)
        self.logger.debug(f"Prompt de validación de historia de usuario: {validation_prompt}")
        
        # Llamar al LLM para obtener la respuesta
        response = self.llm.generate_response(validation_prompt)

        # Manejo de la respuesta para asegurar que sea una cadena
        if isinstance(response, tuple):
            response = response[0]

        self.logger.debug(f"Respuesta de validación de historia de usuario: {response}")

        # Comprobar la respuesta de manera robusta
        response_str = response.strip().lower()
        if response_str in ['true', 'yes', 'valid']:
            return True
        elif response_str in ['false', 'no', 'invalid']:
            return False

        self.logger.error("Respuesta inesperada del modelo: %s", response)
        return False  # O lanza una excepción si prefieres

    def prompt_validation_user_story(self, user_story: str) -> str:
        return f"""
        La historia de usuario debe ser clara, concisa y describir lo que un usuario necesita hacer. 
        Asegúrate de que incluya:
        - Un rol claro (quién está solicitando la historia).
        - Una acción específica (qué quiere hacer el usuario).
        - Un resultado deseado (por qué es importante).

        Historia de usuario actual: {user_story}

        ¿Esta historia de usuario cumple con los criterios mencionados?
        Responde únicamente con 'true' si cumple o 'false' si no cumple, sin ninguna explicación adicional.
        """