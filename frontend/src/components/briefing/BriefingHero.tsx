// Briefing hero (§2, §12): JARVIS-style greeting, headline stats, coverage
// window, and the AI core. The moment the user sees on open.

import { motion } from "framer-motion";
import { AICore } from "@/components/core/AICore";
import { formatDateLong, formatWindowStamp } from "@/lib/format";
import { useAssistant } from "@/stores/ui";
import type { DailyBriefing } from "@/types";

function Stat({ value, label }: { value: number | string; label: string }) {
  return (
    <div className="flex flex-col">
      <span className="text-2xl font-semibold text-text-primary">{value}</span>
      <span className="text-xs text-text-secondary">{label}</span>
    </div>
  );
}

export function BriefingHero({ briefing }: { briefing: DailyBriefing }) {
  const openDock = useAssistant((s) => s.openDock);

  return (
    <motion.section
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-elevated relative overflow-hidden p-6 lg:p-8"
    >
      <div className="pointer-events-none absolute -right-16 -top-16 h-64 w-64 rounded-full bg-primary/10 blur-3xl" />
      <div className="relative flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
        <div className="max-w-xl space-y-4">
          <p className="label-eyebrow">
            AOEN · World Intelligence · {formatDateLong(briefing.generated_at)}
          </p>
          <h1 className="text-3xl font-bold leading-tight text-text-primary lg:text-4xl">
            {briefing.greeting}.
          </h1>
          <p className="text-base leading-relaxed text-text-secondary">
            {briefing.headline}
          </p>

          <div className="flex flex-wrap items-center gap-6 pt-2">
            <Stat value={briefing.stats.total_events} label="developments" />
            <div className="h-8 w-px bg-border/70" />
            <Stat value={briefing.stats.portfolio_events} label="affect your portfolio" />
            <div className="h-8 w-px bg-border/70" />
            <Stat value={briefing.sections.length + 1} label="domains covered" />
          </div>

          <div className="flex flex-wrap items-center gap-3 pt-2">
            <button
              type="button"
              onClick={() => openDock({ question: "Brief me on today's top priorities" })}
              className="rounded-xl border border-primary/40 bg-primary/10 px-4 py-2 text-sm font-medium text-primary transition-colors hover:bg-primary/20 focus-ring"
            >
              Ask AOEN to brief you
            </button>
            <span className="chip">
              Coverage: {formatWindowStamp(briefing.window.start)} →{" "}
              {formatWindowStamp(briefing.window.end)}
            </span>
          </div>
        </div>

        <div className="flex shrink-0 justify-center">
          <AICore state="analyzing" size={150} showLabel />
        </div>
      </div>

      {briefing.notice && (
        <div className="relative mt-5 rounded-xl border border-warning/40 bg-warning/10 p-3 text-sm text-warning">
          {briefing.notice}
        </div>
      )}
    </motion.section>
  );
}
