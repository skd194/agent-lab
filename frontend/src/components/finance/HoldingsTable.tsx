// Holdings table with per-holding intelligence metrics (§6).

import { Newspaper } from "lucide-react";
import { currency, signed, signedPct } from "@/lib/format";
import { cn } from "@/lib/cn";
import type { Holding } from "@/types";

const PRIORITY_STYLE: Record<string, string> = {
  HIGH: "text-primary border-primary/40 bg-primary/10",
  MEDIUM: "text-secondary border-secondary/40 bg-secondary/10",
  LOW: "text-muted border-border/70 bg-surface/50",
};

export function HoldingsTable({
  holdings,
  currencyCode = "INR",
}: {
  holdings: Holding[];
  currencyCode?: string;
}) {
  return (
    <div className="glass overflow-x-auto">
      <table className="w-full min-w-[720px] text-sm">
        <thead>
          <tr className="border-b border-border/60 text-left">
            {["Security", "Price", "Today", "Qty", "Avg", "Value", "Unrealized P/L", "News"].map(
              (h) => (
                <th key={h} className="label-eyebrow px-4 py-3 font-semibold">
                  {h}
                </th>
              ),
            )}
          </tr>
        </thead>
        <tbody>
          {holdings.map((h) => {
            const dayPos = (h.day_change_pct ?? 0) >= 0;
            const plPos = h.unrealized_pl >= 0;
            return (
              <tr
                key={h.id}
                className="border-b border-border/40 transition-colors last:border-0 hover:bg-surface/40"
              >
                <td className="px-4 py-3">
                  <div className="flex items-center gap-2">
                    <div>
                      <p className="font-medium text-text-primary">{h.name}</p>
                      <p className="font-mono text-xs text-muted">
                        {h.symbol} · {h.exchange}
                      </p>
                    </div>
                    <span
                      className={cn(
                        "chip ml-1 hidden text-[10px] sm:inline-flex",
                        PRIORITY_STYLE[h.priority],
                      )}
                    >
                      {h.priority}
                    </span>
                  </div>
                </td>
                <td className="px-4 py-3 font-mono text-text-primary">
                  {currency(h.last_price ?? h.average_price, currencyCode)}
                </td>
                <td className={cn("px-4 py-3 font-mono", dayPos ? "text-success" : "text-danger")}>
                  {signedPct(h.day_change_pct ?? 0)}
                </td>
                <td className="px-4 py-3 font-mono text-text-secondary">{h.quantity}</td>
                <td className="px-4 py-3 font-mono text-text-secondary">
                  {currency(h.average_price, currencyCode)}
                </td>
                <td className="px-4 py-3 font-mono text-text-primary">
                  {currency(h.current_value, currencyCode)}
                </td>
                <td className={cn("px-4 py-3 font-mono", plPos ? "text-success" : "text-danger")}>
                  {signed(h.unrealized_pl, currencyCode)}
                  <span className="ml-1 text-xs opacity-80">
                    ({signedPct(h.unrealized_pl_pct)})
                  </span>
                </td>
                <td className="px-4 py-3">
                  {h.news_count > 0 ? (
                    <span className="chip">
                      <Newspaper size={12} className="text-primary" /> {h.news_count}
                    </span>
                  ) : (
                    <span className="text-xs text-muted">—</span>
                  )}
                </td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
