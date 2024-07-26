# LLAMA 3.1 Self deploy
trying to run Ollama locally for RAG purposes. Interact with the model using rest API (WIP)

https://github.com/user-attachments/assets/3d819203-cd2e-4b5e-992a-1bb64cc4f457

## Installation
### Prerequesite
[Docker](https://www.docker.com/) installed
[Ollama](https://ollama.com/) installed

Download model locally
```
ollama run llama3.1:8b
```

### Run redis
```
docker run --name redis-container -p 6379:6379 -d redis
```

### Run LLM-Service

```bash
cd llm-service
pip install -r requirements.txt
```
```bash
uvicorn llm:app --reload
```
> Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
> 
### Run UI frontend
1. Cd in frontend directory
    ```
    cd frontend
    ```
2. Install dependencies
    ```
    npm install
    ```
3. Run the server
    ```
    npm run dev
    ```
> Go to http://localhost:3000
