import io
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse, Response
from pydantic import BaseModel
from database.mongodb import get_db
from services.SanaBotService import SanaBotService

router = APIRouter(prefix="/sana-bot", tags=["Chat with Sana Bot"])

class ChatRequest(BaseModel):
    message: str
    user_id: str
    insurance_plan: str = "Plan Base"

def get_sanabot_service(db = Depends(get_db)):
    return SanaBotService(db)

@router.post("/chat/{session_id}")
async def chat_endpoint(session_id: str, request: ChatRequest, 
                        service: SanaBotService = Depends(get_sanabot_service)):
    try:
        response_text = await service.chat_with_bot(
            message=request.message, 
            session_id=session_id, 
            user_id=request.user_id,
            insurance_plan=request.insurance_plan
        )
        return {"status": "success", "bot_response": response_text}
    except Exception as e:
        print(f"Error en chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/chat-messages/{session_id}")
async def get_chat_messages_endpoint(session_id: str, service: SanaBotService = Depends(get_sanabot_service)):
    try:
        messages_response = await service.get_chat_messages(session_id=session_id)
        return {"status": "success", "messages": messages_response}
    except Exception as e:
        print(f"Error obteniendo mensajes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

class TTSRequest(BaseModel):
    text: str

@router.post("/tts")
async def tts_endpoint(request: TTSRequest, service: SanaBotService = Depends(get_sanabot_service)):
    try:
        audio_bytes = await service.generate_tts_audio(request.text)
        return Response(content=audio_bytes, media_type="audio/mpeg")
    except Exception as e:
        print(f"Error en TTS: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/stt")
async def stt_endpoint(file: UploadFile = File(...), service: SanaBotService = Depends(get_sanabot_service)):
    try:
        audio_bytes = await file.read()
        text = await service.transcribe_audio(audio_bytes, filename=file.filename)
        return {"status": "success", "text": text}
    except Exception as e:
        print(f"Error en STT: {e}")
        raise HTTPException(status_code=500, detail=str(e))
