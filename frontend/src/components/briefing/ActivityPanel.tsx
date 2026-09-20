// AOEN activity panel (§30): collapsible transparency into what the agents did.

import { AnimatePresence, motion } from "framer-motion";
import { Activity, Check, ChevronDown } from "lucide-react";
import { useState } from "react";
import { cn } from "@/lib/cn";
import type { AgentStep } from "@/types";

export function ActivityPanel({ steps }: { steps: AgentStep[] }) {
  const [open, setOpen] = useState(false);
  if (steps.length === 0) return null;

  return (
    <div className="glass overflow-hidden">
      <button
        type="button"
        onClick={() => setOpen((v) => !v)}
        className="flex w-full items-center gap-3 px-4 py-3 text-left"
      >
        <Activity size={16} className="text-primary" />
        <span className="text-sm font-medium text-text-primary">AOEN activity</span>
        <span className="chip ml-1">{steps.length} steps</span>
        <span className="ml-auto flex items-center gap-2 text-xs text-success">
          <span className="h-1.5 w-1.5 rounded-full bg-success shadow-glow" /> Ready
        </span>
        <ChevronDown
          size={16}
          className={cn("text-muted transition-transform", open && "rotate-180")}
        />
      </button>
      <AnimatePresence initial={false}>
        {open && (
          <motion.ul
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            className="border-t border-border/60 px-4 py-3"
          >
            {steps.map((step, i) => (
              <li
                key={`${step.agent}-${i}`}
                className="flex items-center gap-3 py-1.5 text-sm"
              >
                <Check size={14} className="text-success" />
                <span className="text-text-secondary">{step.message}</span>
                {typeof step.duration_ms === "number" && (
                  <span className="ml-auto font-mono text-[11px] text-muted">
                    {step.duration_ms}ms
                  </span>
                )}
              </li>
            ))}
          </motion.ul>
        )}
      </AnimatePresence>
    </div>
  );
}
