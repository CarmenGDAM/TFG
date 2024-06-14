from fastapi import FastAPI, Query
import uvicorn
import nest_asyncio
import logging
import sys
import http

nest_asyncio.apply()

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env")

from rag import RAG

logging.basicConfig(stream=sys.stdout, level=logging.INFO)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

context_file=""
template = (
    "Eres un asistente virtual, que solo contestas con la información recibida en el contexto. Cualquier otra pregunta que no esté en el contexto ignoralá y responde:'No puedo ayudarte porque no tengo información sobre ese contexto.' \n"
    "A continuación se proporciona la información de contexto. \n"
    "---------------------\n"
    "{context_str}"
    "\n---------------------\n"
    "Usando sólamente esta información, sin aportar nueva información que no aparezca en el contexto, responde a la siguiente consulta: {query_str}\n"
)

# Instanciamos el RAG con el template
rag = RAG(template)

app = FastAPI()


@app.get("/docman")
def ask(query: str):
    response = rag.query(query)
    return {"response": response.response}

@app.post("/docman")
def save(data: str):
    if data is None:
        return {"save": http.HTTPStatus(400, "Bad Request")}
    save = rag.addDocuments(data)
    return {"save": save}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)