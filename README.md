## RAG ChatBot

Getting started
1. Set up the project environment

```
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

2. Start the chatbot backend service (FastAPI)

```
fastapi dev chatbot_api/main.py
```

3. Start the frontend service (Streamlit)

```
streamlit run chatbot_frontend/src/main.py
```
