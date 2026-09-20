// Full-screen voice interaction overlay (§22, §43). Minimal UI, big core,
// transcript + response, push-to-talk, interruption.

import { AnimatePresence, motion } from "framer-motion";
import { Mic, Square, X } from "lucide-react";
import { useEffect } from "react";
import { AICore } from "@/components/core/AICore";
import { useVoice } from "@/hooks/useVoice";
import { useAICore } from "@/stores/aiCore";

export function VoiceOverlay({ open, onClose }: { open: boolean; onClose: () => void }) {
  const { supported, startListening, stopListening, stopSpeaking } = useVoice();
  const { state, transcript, lastResponse, micActive, reset } = useAICore();

  useEffect(() => {
    if (!open) {
      stopListening();
      stopSpeaking();
      reset();
    }
  }, [open, reset, stopListening, stopSpeaking]);

  return (
    <AnimatePresence>
      {open && (
        <motion.div
          className="fixed inset-0 z-[60] flex flex-col items-center justify-center gap-8 bg-background/90 p-6 backdrop-blur-xl"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
        >
          <button
            type="button"
            onClick={onClose}
            aria-label="Close voice"
            className="absolute right-5 top-5 grid h-10 w-10 place-items-center rounded-full border border-border/70 text-text-secondary hover:text-text-primary focus-ring"
          >
            <X size={18} />
          </button>

          <AICore state={state} size={200} showLabel />

          <div className="min-h-[3rem] max-w-lg text-center">
            {transcript && (
              <p className="text-lg text-text-primary">“{transcript}”</p>
            )}
            {lastResponse && (
              <p className="mt-3 text-base text-text-secondary">{lastResponse}</p>
            )}
            {!transcript && !lastResponse && (
              <p className="text-text-secondary">
                {supported
                  ? "Hold the mic and say “Good morning, AOEN” or “Brief me.”"
                  : "Voice isn't supported in this browser. Try the Ask AOEN dock instead."}
              </p>
            )}
          </div>

          {supported && (
            <div className="flex items-center gap-4">
              <button
                type="button"
                onPointerDown={startListening}
                onPointerUp={stopListening}
                className="grid h-20 w-20 place-items-center rounded-full border border-primary/50 bg-primary/10 text-primary shadow-glow-strong transition-transform active:scale-95"
                aria-label="Push to talk"
              >
                <Mic size={30} />
              </button>
              {state === "speaking" && (
                <button
                  type="button"
                  onClick={stopSpeaking}
                  className="grid h-14 w-14 place-items-center rounded-full border border-border/70 text-text-secondary hover:text-danger focus-ring"
                  aria-label="Stop speaking"
                >
                  <Square size={20} />
                </button>
              )}
            </div>
          )}
          <p className="text-xs text-muted">
            {micActive ? "Listening…" : "Press and hold to talk"}
          </p>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
