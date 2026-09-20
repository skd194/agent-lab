"""Voice endpoints (§22, §33).

STT/TTS run client-side (browser Web Speech API) in demo mode; these endpoints
provide command routing and a TTS passthrough contract.
"""

from fastapi import APIRouter

from app.schemas.voice import (
    SpeakRequest,
    SpeakResponse,
    VoiceCommand,
    VoiceCommandResult,
)
from app.services.voice_service import voice_service

router = APIRouter(prefix="/voice", tags=["voice"])


@router.post("/command", response_model=VoiceCommandResult)
async def route_command(payload: VoiceCommand) -> VoiceCommandResult:
    """Route a transcript to an intent (§21)."""
    return voice_service.route(payload.transcript)


@router.post("/speak", response_model=SpeakResponse)
async def speak(payload: SpeakRequest) -> SpeakResponse:
    """Return TTS instructions. Demo mode delegates to the browser (§22)."""
    return SpeakResponse(audio_url=None, text=payload.text, engine="browser")
