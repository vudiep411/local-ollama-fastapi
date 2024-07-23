# AI RAG
trying to run Ollama locally for RAG purposes. Interact with the model using rest API (WIP)

https://github.com/user-attachments/assets/7229c5d7-a197-48ba-a3f5-797703ad97c3

## Test API
```bash
cd llm-service
pip install -r requirements.txt
```
```bash
uvicorn llm:app --reload
```

Go to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)