// Event detail modal (§7, §14, §15). Clearly separates FACT / AI ANALYSIS /
// PORTFOLIO RELEVANCE, lists affected holdings and every source.

import { AnimatePresence, motion } from "framer-motion";
import { ExternalLink, MessageSquare, X } from "lucide-react";
import { domainMeta } from "@/lib/domains";
import { relativeTime } from "@/lib/format";
import { useAssistant, useEventModal } from "@/stores/ui";
import { FinanceTierBadge, ImpactBadge, RelevanceBar, VerifiedBadge } from "./badges";

function Section({ eyebrow, children }: { eyebrow: string; children: React.ReactNode }) {
  return (
    <div className="rounded-xl border border-border/50 bg-surface/40 p-4">
      <p className="label-eyebrow mb-2">{eyebrow}</p>
      <div className="text-sm leading-relaxed text-text-secondary">{children}</div>
    </div>
  );
}

export function EventModal() {
  const event = useEventModal((s) => s.event);
  const close = useEventModal((s) => s.close);
  const openDock = useAssistant((s) => s.openDock);

  return (
    <AnimatePresence>
      {event && (
        <motion.div
          className="fixed inset-0 z-50 flex items-end justify-center bg-black/60 p-0 backdrop-blur-sm sm:items-center sm:p-6"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={close}
        >
          <motion.div
            className="glass-elevated max-h-[92vh] w-full max-w-2xl overflow-y-auto rounded-t-card sm:rounded-card"
            initial={{ y: 40, opacity: 0, scale: 0.98 }}
            animate={{ y: 0, opacity: 1, scale: 1 }}
            exit={{ y: 40, opacity: 0 }}
            onClick={(e) => e.stopPropagation()}
          >
            <div className="sticky top-0 flex items-start justify-between gap-3 border-b border-border/60 bg-surface-elevated/80 p-5 backdrop-blur-glass">
              <div className="flex flex-wrap items-center gap-2">
                {(() => {
                  const meta = domainMeta(event.category);
                  return (
                    <span className="chip">
                      <meta.icon size={13} className="text-primary" /> {meta.label}
                    </span>
                  );
                })()}
                <VerifiedBadge verified={event.verified} />
                {event.insight?.finance_tier && (
                  <FinanceTierBadge tier={event.insight.finance_tier} />
                )}
              </div>
              <button
                type="button"
                onClick={close}
                aria-label="Close"
                className="grid h-8 w-8 shrink-0 place-items-center rounded-full border border-border/70 text-text-secondary hover:text-text-primary focus-ring"
              >
                <X size={16} />
              </button>
            </div>

            <div className="space-y-4 p-5">
              <h2 className="text-xl font-semibold leading-snug text-text-primary">
                {event.title}
              </h2>
              <RelevanceBar tier={event.relevance_tier} />

              <Section eyebrow="Fact — what happened">
                {event.insight?.what_happened ?? event.summary ?? "—"}
              </Section>

              {event.insight?.ai_analysis && (
                <Section eyebrow="AI analysis — AOEN's interpretation">
                  {event.insight.ai_analysis}
                </Section>
              )}

              {event.insight?.portfolio_relevance && (
                <Section eyebrow="Portfolio relevance">
                  {event.insight.portfolio_relevance}
                </Section>
              )}

              {event.insight?.impacts && event.insight.impacts.length > 0 && (
                <div className="rounded-xl border border-border/50 bg-surface/40 p-4">
                  <p className="label-eyebrow mb-3">Affected holdings</p>
                  <div className="space-y-2">
                    {event.insight.impacts.map((impact) => (
                      <div
                        key={impact.holding_symbol}
                        className="flex items-center justify-between gap-3"
                      >
                        <div>
                          <p className="font-mono text-sm text-text-primary">
                            {impact.holding_symbol}
                          </p>
                          {impact.rationale && (
                            <p className="text-xs text-muted">{impact.rationale}</p>
                          )}
                        </div>
                        <ImpactBadge impact={impact.impact_type} />
                      </div>
                    ))}
                  </div>
                  <p className="mt-3 text-[11px] text-muted">
                    Informational classification only — not investment advice.
                  </p>
                </div>
              )}

              {event.entities.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {event.entities.map((e) => (
                    <span key={e} className="chip">
                      {e}
                    </span>
                  ))}
                </div>
              )}

              <div>
                <p className="label-eyebrow mb-2">
                  {event.sources.length} source
                  {event.sources.length === 1 ? "" : "s"} reporting this event
                </p>
                <div className="space-y-2">
                  {event.sources.map((s) => (
                    <a
                      key={s.url}
                      href={s.url}
                      target="_blank"
                      rel="noreferrer"
                      className="flex items-center justify-between gap-3 rounded-xl border border-border/50 bg-surface/40 p-3 transition-colors hover:border-primary/40"
                    >
                      <div className="min-w-0">
                        <p className="truncate text-sm text-text-primary">{s.title}</p>
                        <p className="text-xs text-muted">
                          {s.source_name}
                          {s.published_at ? ` · ${relativeTime(s.published_at)}` : ""}
                        </p>
                      </div>
                      <ExternalLink size={15} className="shrink-0 text-primary" />
                    </a>
                  ))}
                </div>
              </div>

              <button
                type="button"
                onClick={() => {
                  openDock({ event, question: `Tell me more about: ${event.title}` });
                  close();
                }}
                className="flex w-full items-center justify-center gap-2 rounded-xl border border-primary/40 bg-primary/10 py-3 text-sm font-medium text-primary transition-colors hover:bg-primary/20 focus-ring"
              >
                <MessageSquare size={16} /> Ask AOEN about this
              </button>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
}
