// Top bar (§18): brand, system status pill, live clock, quick voice trigger.

import { Mic } from "lucide-react";
import { useEffect, useState } from "react";
import { useSystemStatus } from "@/services/queries";
import { formatClock } from "@/lib/format";
import { useAICore } from "@/stores/aiCore";
import { cn } from "@/lib/cn";

export function TopBar({ onVoice }: { onVoice: () => void }) {
  const { data: status } = useSystemStatus();
  const [clock, setClock] = useState(formatClock());
  const micActive = useAICore((s) => s.micActive);

  useEffect(() => {
    const id = setInterval(() => setClock(formatClock()), 1000);
    return () => clearInterval(id);
  }, []);

  const online = status?.status === "online";

  return (
    <header className="flex items-center justify-between gap-4 border-b border-border/60 bg-surface/30 px-4 py-3 backdrop-blur-glass lg:px-6">
      <div className="flex items-center gap-3 lg:hidden">
        <span className="text-base font-bold tracking-[0.24em]">AOEN</span>
      </div>

      <div className="ml-auto flex items-center gap-3">
        {status?.demo_mode && (
          <span className="chip border-warning/40 text-warning">DEMO MODE</span>
        )}
        <span className="chip">
          <span
            className={cn(
              "h-1.5 w-1.5 rounded-full",
              online ? "bg-success shadow-glow" : "bg-danger",
            )}
          />
          {online ? "SYSTEM ONLINE" : "OFFLINE"}
        </span>
        <span className="hidden font-mono text-sm text-text-secondary sm:inline">
          {clock}
        </span>
        <button
          type="button"
          onClick={onVoice}
          aria-label="Talk to AOEN"
          className={cn(
            "grid h-9 w-9 place-items-center rounded-full border border-border/70 bg-surface/60 text-primary transition-colors hover:bg-primary/10 focus-ring",
            micActive && "bg-primary/20 shadow-glow",
          )}
        >
          <Mic size={18} />
        </button>
      </div>
    </header>
  );
}
