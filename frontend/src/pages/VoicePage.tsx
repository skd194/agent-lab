// Voice page (§20, §21): explains and launches the voice experience, lists the
// supported commands (extensible).

import { Mic } from "lucide-react";
import { useState } from "react";
import { AICore } from "@/components/core/AICore";
import { Panel } from "@/components/ui/Panel";
import { VoiceOverlay } from "@/components/voice/VoiceOverlay";
import { useAICore } from "@/stores/aiCore";

const COMMANDS = [
  "Good morning, AOEN.",
  "Brief me.",
  "Give me the finance briefing.",
  "What's happening with Tata Steel?",
  "What changed in India?",
  "Tell me the top three stories.",
  "Explain this.",
  "Summarize everything in two minutes.",
  "Read my portfolio news.",
];

export function VoicePage() {
  const [open, setOpen] = useState(false);
  const state = useAICore((s) => s.state);

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <p className="label-eyebrow">AOEN · Voice</p>
        <h1 className="text-2xl font-bold text-text-primary">Talk to AOEN</h1>
      </header>

      <Panel className="flex flex-col items-center gap-6 py-10 text-center">
        <AICore state={state} size={150} showLabel />
        <p className="max-w-md text-text-secondary">
          Ask for your briefing hands-free. AOEN listens only while you hold the
          mic and never records continuously without your consent.
        </p>
        <button
          type="button"
          onClick={() => setOpen(true)}
          className="flex items-center gap-2 rounded-xl border border-primary/40 bg-primary/10 px-6 py-3 text-sm font-medium text-primary hover:bg-primary/20 focus-ring"
        >
          <Mic size={18} /> Start voice session
        </button>
      </Panel>

      <Panel eyebrow="Commands" title="Try saying">
        <div className="grid gap-2 sm:grid-cols-2">
          {COMMANDS.map((c) => (
            <div key={c} className="chip justify-start">
              “{c}”
            </div>
          ))}
        </div>
      </Panel>

      <VoiceOverlay open={open} onClose={() => setOpen(false)} />
    </div>
  );
}
