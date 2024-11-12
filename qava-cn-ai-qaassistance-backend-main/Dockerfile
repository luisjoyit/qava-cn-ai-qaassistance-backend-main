FROM python:3.10-bookworm

WORKDIR /app

RUN apt-get update && \
    apt-get install -y \
    curl \
    gnupg2 \
    lsb-release \
    software-properties-common \
    git \
    procps && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
EJECUTAR curl -SL "https://nodejs.org/dist/v ${VERSIÓN_DE_NODO} /node-v ${VERSIÓN_DE_NODO} -linux-x64.tar.gz" --output nodejs.tar.gz \
&& echo  " $NODE_DOWNLOAD_SHA nodejs.tar.gz" | sha256sum -c - \
&& tar -xzf "nodejs.tar.gz" -C /usr/local --strip-components=1 \
&& rm nodejs.tar.gz \
&& ln -s /usr/local/bin/node /usr/local/bin/nodejs

RUN pip install nltk && \
    python3 -c "import nltk; nltk.download('punkt_tab')"

COPY ./ollama.py /usr/local/lib/python3.10/site-packages/langchain_community/embeddings/ollama.py

COPY app.py .
COPY src ./src

EXPOSE 5000

CMD ["sh", "-c", "flask run --host=0.0.0.0 --port=5000"]