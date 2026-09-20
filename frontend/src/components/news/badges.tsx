// Small status badges for news (§7, §14, §16).

import { cn } from "@/lib/cn";
import type { FinanceTier, ImpactType, RelevanceTier } from "@/types";

const TIER_STYLE: Record<RelevanceTier, string> = {
  high: "text-primary border-primary/40 bg-primary/10",
  medium: "text-secondary border-secondary/40 bg-secondary/10",
  low: "text-muted border-border/70 bg-surface/50",
};

export function RelevanceBar({ tier }: { tier: RelevanceTier }) {
  const filled = tier === "high" ? 5 : tier === "medium" ? 3 : 1;
  return (
    <div className="flex items-center gap-2">
      <div className="flex gap-1" aria-hidden>
        {Array.from({ length: 5 }).map((_, i) => (
          <span
            key={i}
            className={cn(
              "h-1.5 w-4 rounded-full",
              i < filled ? "bg-primary shadow-glow" : "bg-border/70",
            )}
          />
        ))}
      </div>
      <span className={cn("text-[11px] font-semibold uppercase tracking-wider", TIER_STYLE[tier].split(" ")[0])}>
        {tier} relevance
      </span>
    </div>
  );
}

const IMPACT_STYLE: Record<ImpactType, string> = {
  positive: "text-success border-success/40 bg-success/10",
  negative: "text-danger border-danger/40 bg-danger/10",
  neutral: "text-text-secondary border-border/70 bg-surface/50",
  mixed: "text-warning border-warning/40 bg-warning/10",
  watch: "text-secondary border-secondary/40 bg-secondary/10",
};

export function ImpactBadge({ impact }: { impact: ImpactType }) {
  return (
    <span className={cn("chip uppercase tracking-wider", IMPACT_STYLE[impact])}>
      {impact}
    </span>
  );
}

const FINANCE_TIER_LABEL: Record<FinanceTier, string> = {
  direct_holding: "Direct holding",
  sector: "Sector",
  macro: "Macro",
  general: "General",
};

export function FinanceTierBadge({ tier }: { tier: FinanceTier }) {
  return (
    <span
      className={cn(
        "chip uppercase tracking-wider",
        tier === "direct_holding" && "text-primary border-primary/40 bg-primary/10",
        tier === "sector" && "text-secondary border-secondary/40 bg-secondary/10",
      )}
    >
      {FINANCE_TIER_LABEL[tier]}
    </span>
  );
}

export function VerifiedBadge({ verified }: { verified: boolean }) {
  if (verified) return null;
  return (
    <span className="chip border-warning/40 bg-warning/10 uppercase tracking-wider text-warning">
      Unverified
    </span>
  );
}
