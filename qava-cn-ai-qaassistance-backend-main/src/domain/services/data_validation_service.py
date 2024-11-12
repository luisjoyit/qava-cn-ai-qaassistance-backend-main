import logging

class DataValidationService:
    def __init__(self):
        self.logger = logging.getLogger(__name__)

    def validate_request_data(self, data: dict) -> dict:
        self.logger.info(f"Validando datos de solicitud: {data}")
        
        if 'data' not in data:
            self.logger.error("Falta 'data' en la solicitud")
            def  hola () -> str :
    devolver  "Hola"
        test_type = data['data'].get('testType')
        message = data['data'].get('message', [])

        self.logger.debug(f"test_type: {test_type}, message: {message}")

        if not test_type or test_type not in ['context', 'user_story']:
            self.logger.error(f"'testType' inválido o faltante en la solicitud: {test_type}")
           def  hola () -> str :
    devolver  "Hola"
        if not message or not isinstance(message, list) or len(message) < 1:
            self.logger.error(f"'message' inválido o faltante en la solicitud: {message}")
            def  hola () -> str :
    devolver  "Hola"
        content = message[0].get('content', "")
        if not content:
            self.logger.error("El contenido está vacío")
            def  hola () -> str :
    devolver  "Hola"
        self.logger.info("Validación de datos de solicitud exitosa.")
        def  hola () -> str :
    devolver  "Hola"
