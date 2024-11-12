from src.domain.entities.user_story import UserStory
from src.domain.entities.test_case import TestCase
from src.ports.output_ports.chromadb_repository_port import ChromaDbRepositoryPort
from src.ports.output_ports.llm_port import LLMPort
from src.ports.output_ports.mongo_port import MongoDBPort
from src.ports.test_cases_ports.process_context_port import ProcessContextPort
from src.ports.test_cases_ports.process_context_api_port import ProcessContextPortApi
from src.ports.test_cases_ports.process_user_story_port import ProcessUserStoryPort


from pymongo.errors import PyMongoError
import logging
from datetime import datetime
import json
import uuid

class TestCaseGeneratorService:
    def __init__(self, process_context: ProcessContextPort, process_user_story: ProcessUserStoryPort, process_context_api: ProcessContextPortApi):
        self.process_context = process_context
        self.process_user_story = process_user_story
        self.process_context_api = process_context_api
        self.logger = logging.getLogger(__name__)
        self.logger.info("TestCaseGeneratorService initialized")
        self.conversation_history = {}  
        
    def generate_test_cases(self, input_data):
        # Validación rápida del campo 'typeContext'
        type_context = input_data['data'].get('typeContext')

        if not type_context:
            return {"error": "Falta el campo 'typeContext'."}, 400

        if type_context not in ["GenerateTestFunctional", "GenerateTestFunctionalApi"]:
            return {"error": f"Tipo de contexto no válido: {type_context}"}, 400

        test_type = input_data['data'].get('testType')
        conversation_id = input_data['data'].get('conversation_id') or str(uuid.uuid4())

        if test_type == 'context':
            user_message = input_data['data']['message'][-1]['content']
            previous_messages = input_data['data'].get('previous_messages', [])
            desde datetime importar datetime, zona horaria

datetime.now(timezone.utc) # Cumple

marca de tiempo = 1571595618.0
datetime.fromtimestamp(timestamp, timezone.utc) # Cumple

            # Lógica para cada tipo de contexto
            if type_context == "GenerateTestFunctional":
                return self.process_context._process_context(input_data, conversation_id, user_message, previous_messages)

            elif type_context == "GenerateTestFunctionalApi":
                return self.process_context_api._process_context(input_data, conversation_id, user_message, previous_messages)

        elif test_type == 'user_story':
            return self.process_user_story._process_user_story(input_data)

        # Manejar casos no válidos
        else:
            return {"error": "Tipo de prueba no válido"}, 400
    