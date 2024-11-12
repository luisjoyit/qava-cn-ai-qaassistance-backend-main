# src/adapters/name_history_generator_adapter.py

from src.ports.conversation_ports.name_history_generator_port import NameHistoryGeneratorPort
from src.ports.output_ports.llm_port import LLMPort

class NameHistoryGeneratorAdapter(NameHistoryGeneratorPort):
    def __init__(self, llm: LLMPort):
        self.llm = llm

    def generate_name_history(self, context_data):
    
        prompt = f"""Basado en el contexto: {context_data}, genera únicamente un solo nombre, "
        "conciso, claro, y relacionado exclusivamente con el contexto. El nombre no "
        "debe contener más de cuatro palabras. No añadas listas, explicaciones ni "
        "otros detalles adicionales."""
        
        name_history = self.llm.generate_response(prompt)
        
        # Si name_history es un tuple, selecciona el primer elemento.
        if isinstance(name_history, tuple):
            name_history = name_history[0]
        
        return name_history.strip()
