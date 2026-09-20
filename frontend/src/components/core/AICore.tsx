// AOEN AI core (§19) — a circular core with concentric rings whose motion and
// colour reflect the current system state. Subtle by default (breathing), more
// active while working. Respects prefers-reduced-motion via CSS (§42).

import { motion } from "framer-motion";
import { cn } from "@/lib/cn";
import type { AICoreState } from "@/types";

const STATE_LABEL: Record<AICoreState, string> = {
  idle: "STANDBY",
  listening: "LISTENING",
  searching: "SEARCHING",
  thinking: "THINKING",
  analyzing: "ANALYZING",
  speaking: "SPEAKING",
  error: "ERROR",
};

const STATE_COLOR: Record<AICoreState, string> = {
  idle: "var(--aoen-primary)",
  listening: "var(--aoen-success)",
  searching: "var(--aoen-primary)",
  thinking: "var(--aoen-secondary)",
  analyzing: "var(--aoen-secondary)",
  speaking: "var(--aoen-primary)",
  error: "var(--aoen-danger)",
};

interface Props {
  state: AICoreState;
  size?: number;
  showLabel?: boolean;
  className?: string;
}

export function AICore({ state, size = 120, showLabel = false, className }: Props) {
  const color = `rgb(${STATE_COLOR[state]})`;
  const active = state !== "idle";
  const speaking = state === "speaking";

  return (
    <div className={cn("flex flex-col items-center gap-3", className)}>
      <div
        className="relative grid place-items-center"
        style={{ width: size, height: size }}
        role="img"
        aria-label={`AOEN ${STATE_LABEL[state]}`}
      >
        {/* Expanding pulse ring while active */}
        {active && (
          <span
            className="absolute inset-0 rounded-full animate-pulse-ring"
            style={{ boxShadow: `0 0 0 1px ${color}`, background: `radial-gradient(circle, ${color}22, transparent 70%)` }}
          />
        )}

        {/* Outer rotating ring */}
        <motion.div
          className="absolute rounded-full border"
          style={{
            width: size,
            height: size,
            borderColor: `${color}55`,
            borderTopColor: color,
          }}
          animate={{ rotate: 360 }}
          transition={{ duration: active ? 3 : 14, ease: "linear", repeat: Infinity }}
        />

        {/* Middle counter-rotating ring */}
        <motion.div
          className="absolute rounded-full border border-dashed"
          style={{
            width: size * 0.72,
            height: size * 0.72,
            borderColor: `${color}44`,
          }}
          animate={{ rotate: -360 }}
          transition={{ duration: active ? 5 : 22, ease: "linear", repeat: Infinity }}
        />

        {/* Core orb */}
        <motion.div
          className={cn("relative rounded-full", !active && "animate-breathe")}
          style={{
            width: size * 0.44,
            height: size * 0.44,
            background: `radial-gradient(circle at 35% 30%, ${color}, ${color}33 70%, transparent)`,
            boxShadow: `0 0 ${size * 0.28}px ${color}77`,
          }}
          animate={active ? { scale: [1, 1.08, 1] } : {}}
          transition={{ duration: 1.4, repeat: Infinity, ease: "easeInOut" }}
        />

        {/* Speaking waveform overlay */}
        {speaking && (
          <div className="absolute flex items-center gap-[3px]">
            {[0, 1, 2, 3, 4].map((i) => (
              <motion.span
                key={i}
                className="w-[3px] rounded-full"
                style={{ background: color }}
                animate={{ height: [6, size * 0.22, 6] }}
                transition={{
                  duration: 0.6,
                  repeat: Infinity,
                  ease: "easeInOut",
                  delay: i * 0.12,
                }}
              />
            ))}
          </div>
        )}
      </div>

      {showLabel && (
        <div className="flex items-center gap-2">
          <span
            className="h-1.5 w-1.5 rounded-full"
            style={{ background: color, boxShadow: `0 0 8px ${color}` }}
          />
          <span className="label-eyebrow" style={{ color }}>
            {STATE_LABEL[state]}
          </span>
        </div>
      )}
    </div>
  );
}
