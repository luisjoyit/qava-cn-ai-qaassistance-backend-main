# ia-asv-cn-qaassistance
### Ejecutar
##### Crear network
```sh
docker network create qava_net
```

##### Compilar
```sh
docker buildx create --name localbuilder --use
docker buildx inspect localbuilder --bootstrap
docker buildx build --platform linux/amd64 -t ia-asv-cn-qaassistance:latest .
docker buildx build --platform linux/arm64 -t ia-asv-cn-qaassistance:latest .
docker compose build
docker build -t ia-asv-cn-qaassistance:latest .
docker run --rm ia-asv-cn-qaassistance:latest
```

##### Ejecutar contenedor
```sh
start.sh
```

##### Probar chromadb
En el navegador:
```sh
http://localhost:8000/api/v1/heartbeat
```

En la consola:
```sh
curl http://localhost:8000/api/v1/heartbeat
```

##### Probar modelos de ollana
En el navegador:
```sh
http://localhost:11434//api/tags
```

En la consola:
```sh
curl http://localhost:11434//api/tags
```

```
qava-cn-ai-qaassistance-backend
├─ .env
├─ .gitignore
├─ app.py
├─ docker-compose.yml
├─ Dockerfile
├─ install-ollama.sh
├─ install.sh
├─ ollama-local
│  ├─ id_ed25519
│  └─ id_ed25519.pub
├─ ollama.py
├─ README.md
├─ requirements.txt
├─ src
│  ├─ adapters
│  │  ├─ conversation_adapters
│  │  │  ├─ conversation_management_adapter.py
│  │  │  └─ name_history_generator_adapter.py
│  │  ├─ image_adapters
│  │  │  ├─ docx_to_image_adapter.py
│  │  │  ├─ doc_to_image_adapter.py
│  │  │  ├─ image_to_text_adapter.py
│  │  │  ├─ pdf_to_image_adapter.py
│  │  │  ├─ pptx_to_image_adapter.py
│  │  │  └─ ppt_to_image_adapter.py
│  │  ├─ input_adapters
│  │  │  ├─ api_controller.py
│  │  │  └─ __init__.py
│  │  ├─ output_adapters
│  │  │  ├─ chroma_repository.py
│  │  │  ├─ kafka_repository.py
│  │  │  ├─ mongo_repository.py
│  │  │  ├─ ollama_repository.py
│  │  │  └─ __init__.py
│  │  ├─ test_cases_adapters
│  │  │  ├─ process_context_adapter.py
│  │  │  ├─ process_user_story_adapter.py
│  │  │  └─ test_case_prompt_generator_adapter.py
│  │  └─ _init__.py
│  ├─ domain
│  │  ├─ entities
│  │  │  ├─ test_case.py
│  │  │  ├─ user_story.py
│  │  │  └─ __init__.py
│  │  └─ services
│  │     └─ data_validation_service.py
│  ├─ ports
│  │  ├─ context_validation_port.py
│  │  ├─ conversation_management_port.py
│  │  ├─ docx_to_image_port.py
│  │  ├─ doc_to_image_port.py
│  │  ├─ input_ports
│  │  │  ├─ api_port.py
│  │  │  └─ __init__.py
│  │  ├─ name_history_generator_port.py
│  │  ├─ output_ports
│  │  │  ├─ chromadb_repository_port.py
│  │  │  ├─ conversation_repository_port.py
│  │  │  ├─ llm_port.py
│  │  │  ├─ mongo_port.py
│  │  │  └─ __init__.py
│  │  ├─ pdf_to_image_port.py
│  │  ├─ pptx_to_image_port.py
│  │  ├─ ppt_to_image_port.py
│  │  ├─ test_case_prompt_generator_port.py
│  │  ├─ user_story_validation_port.py
│  │  └─ __init__.py
│  ├─ services
│  │  ├─ image_to_text_service.py
│  │  ├─ send_kafka_mongo_service_.py
│  │  ├─ test_case_generator_service.py
│  │  ├─ to_image_service.py
│  │  └─ __init__.py
│  └─ __init__.py
├─ start.sh
├─ stop.sh
└─ test.py

```