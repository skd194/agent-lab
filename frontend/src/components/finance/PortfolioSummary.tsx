// Portfolio overview — intelligence-terminal style, not a trading site (§6).

import { motion } from "framer-motion";
import { ArrowDownRight, ArrowUpRight } from "lucide-react";
import { currency, signed, signedPct } from "@/lib/format";
import { cn } from "@/lib/cn";
import type { PortfolioOverview } from "@/types";

function Metric({
  label,
  value,
  delta,
  positive,
}: {
  label: string;
  value: string;
  delta?: string;
  positive?: boolean;
}) {
  return (
    <div className="glass p-4">
      <p className="label-eyebrow">{label}</p>
      <p className="mt-2 text-2xl font-semibold text-text-primary">{value}</p>
      {delta && (
        <p
          className={cn(
            "mt-1 flex items-center gap-1 text-sm",
            positive ? "text-success" : "text-danger",
          )}
        >
          {positive ? <ArrowUpRight size={14} /> : <ArrowDownRight size={14} />}
          {delta}
        </p>
      )}
    </div>
  );
}

export function PortfolioSummary({ overview }: { overview: PortfolioOverview }) {
  const cur = overview.base_currency;
  const dayPos = overview.day_change_value >= 0;
  const totalPos = overview.overall_pl >= 0;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4"
    >
      <Metric label="Invested value" value={currency(overview.total_invested, cur)} />
      <Metric label="Current value" value={currency(overview.current_value, cur)} />
      <Metric
        label="Today"
        value={signed(overview.day_change_value, cur)}
        delta={signedPct(overview.day_change_pct)}
        positive={dayPos}
      />
      <Metric
        label="Overall P/L"
        value={signed(overview.overall_pl, cur)}
        delta={signedPct(overview.overall_pl_pct)}
        positive={totalPos}
      />
    </motion.div>
  );
}
