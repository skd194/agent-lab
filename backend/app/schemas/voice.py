"""Voice API schemas (§20, §21, §22)."""

from pydantic import BaseModel


class TranscribeResponse(BaseModel):
    """Speech-to-text result."""

    transcript: str
    confidence: float = 1.0


class SpeakRequest(BaseModel):
    """Text-to-speech request."""

    text: str
    voice: str = "aoen"


class SpeakResponse(BaseModel):
    """Text-to-speech result (client may also use browser SpeechSynthesis)."""

    audio_url: str | None = None
    text: str
    engine: str = "browser"  # demo mode delegates to the browser's TTS


class VoiceCommand(BaseModel):
    """A parsed voice command routed to an intent (§21)."""

    transcript: str


class VoiceCommandResult(BaseModel):
    """Routing result for a voice command (§21)."""

    intent: str
    args: dict = {}
    spoken_response: str
