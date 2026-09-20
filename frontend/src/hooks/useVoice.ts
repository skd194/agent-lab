// Voice interaction hook (§20, §22). Uses the browser Web Speech API for STT
// and TTS so no audio is sent to a server, and mic is only active on demand
// (never continuous recording without consent §22). Interruptible (§20).

import { useCallback, useEffect, useRef, useState } from "react";
import { api } from "@/services/api";
import { useAICore } from "@/stores/aiCore";

// Minimal typings for the (non-standard) SpeechRecognition API.
interface SpeechRecognitionLike {
  lang: string;
  interimResults: boolean;
  continuous: boolean;
  onresult: ((e: any) => void) | null;
  onerror: ((e: any) => void) | null;
  onend: (() => void) | null;
  start: () => void;
  stop: () => void;
}

function getRecognition(): SpeechRecognitionLike | null {
  const w = window as any;
  const Ctor = w.SpeechRecognition || w.webkitSpeechRecognition;
  if (!Ctor) return null;
  const rec: SpeechRecognitionLike = new Ctor();
  rec.lang = "en-IN";
  rec.interimResults = true;
  rec.continuous = false;
  return rec;
}

export function useVoice() {
  const recognitionRef = useRef<SpeechRecognitionLike | null>(null);
  const { setState, setTranscript, setResponse, setMicActive } = useAICore();
  const [supported, setSupported] = useState(true);

  useEffect(() => {
    const ttsOk = typeof window !== "undefined" && "speechSynthesis" in window;
    const sttOk = getRecognition() !== null;
    setSupported(ttsOk || sttOk);
  }, []);

  const speak = useCallback(
    (text: string) => {
      if (!("speechSynthesis" in window)) return;
      window.speechSynthesis.cancel();
      const utter = new SpeechSynthesisUtterance(text);
      utter.lang = "en-IN";
      utter.rate = 1.02;
      utter.onstart = () => setState("speaking");
      utter.onend = () => setState("idle");
      window.speechSynthesis.speak(utter);
    },
    [setState],
  );

  const stopSpeaking = useCallback(() => {
    if ("speechSynthesis" in window) window.speechSynthesis.cancel();
    setState("idle");
  }, [setState]);

  const handleTranscript = useCallback(
    async (text: string) => {
      setTranscript(text);
      setState("thinking");
      try {
        const result = await api.voiceCommand(text);
        setResponse(result.spoken_response);
        speak(result.spoken_response);
      } catch {
        const msg = "I couldn't process that just now.";
        setResponse(msg);
        setState("error");
      }
    },
    [setResponse, setState, setTranscript, speak],
  );

  const startListening = useCallback(() => {
    // Interrupt any current speech (§20) before listening.
    stopSpeaking();
    const rec = getRecognition();
    if (!rec) {
      setSupported(false);
      return;
    }
    recognitionRef.current = rec;
    setMicActive(true);
    setState("listening");
    setTranscript("");

    let finalText = "";
    rec.onresult = (e: any) => {
      let interim = "";
      for (let i = e.resultIndex; i < e.results.length; i++) {
        const chunk = e.results[i][0].transcript;
        if (e.results[i].isFinal) finalText += chunk;
        else interim += chunk;
      }
      setTranscript(finalText || interim);
    };
    rec.onerror = () => {
      setMicActive(false);
      setState("error");
    };
    rec.onend = () => {
      setMicActive(false);
      if (finalText.trim()) void handleTranscript(finalText.trim());
      else setState("idle");
    };
    rec.start();
  }, [handleTranscript, setMicActive, setState, setTranscript, stopSpeaking]);

  const stopListening = useCallback(() => {
    recognitionRef.current?.stop();
    setMicActive(false);
  }, [setMicActive]);

  return { supported, startListening, stopListening, speak, stopSpeaking };
}
