import chromadb

try:
    chroma_client = chromadb.HttpClient(
        host='localhost',
        port=8000
    )
    print("Conexión exitosa a ChromaDB.")
except Exception as e:
    print(f"Error al conectar a ChromaDB: {e}")