from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from firebase_service import verify_token, get_active_partida
from openrouter_service import ask_llm
from context_builder import build_context

app = FastAPI(title="ProfessionalNuzlocker Backend")
bearer = HTTPBearer()


class ChatRequest(BaseModel):
    message: str
    partida_id: str


@app.post("/chat")
async def chat(request: ChatRequest, credentials: HTTPAuthorizationCredentials = Depends(bearer)):
    token = credentials.credentials
    uid = verify_token(token)
    if not uid:
        raise HTTPException(status_code=401, detail="Token inválido")

    partida = get_active_partida(uid, request.partida_id)
    if not partida:
        raise HTTPException(status_code=404, detail="Partida no encontrada")

    context = build_context(partida)
    response = ask_llm(context, request.message)

    return {"response": response}


@app.get("/health")
def health():
    return {"status": "ok"}
