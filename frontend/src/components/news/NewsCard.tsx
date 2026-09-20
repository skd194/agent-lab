// Compact intelligence card (§13). Headline, AI summary, why-it-matters,
// source + timestamp, relevance, and actions (Read Source / Ask AOEN).

import { motion } from "framer-motion";
import { ExternalLink, Layers, MessageSquare } from "lucide-react";
import { domainMeta } from "@/lib/domains";
import { relativeTime } from "@/lib/format";
import { useAssistant, useEventModal } from "@/stores/ui";
import type { EventOut } from "@/types";
import { FinanceTierBadge, RelevanceBar, VerifiedBadge } from "./badges";

export function NewsCard({ event, index = 0 }: { event: EventOut; index?: number }) {
  const openModal = useEventModal((s) => s.open);
  const openDock = useAssistant((s) => s.openDock);
  const meta = domainMeta(event.category);
  const primary = event.sources[0];

  return (
    <motion.article
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.04, 0.3) }}
      className="glass group flex h-full flex-col gap-3 p-4 transition-colors duration-250 hover:border-primary/40"
    >
      <div className="flex items-center justify-between gap-2">
        <span className="chip">
          <meta.icon size={13} className="text-primary" />
          {meta.label}
        </span>
        <div className="flex items-center gap-2">
          <VerifiedBadge verified={event.verified} />
          {event.insight?.finance_tier && (
            <FinanceTierBadge tier={event.insight.finance_tier} />
          )}
        </div>
      </div>

      <button
        type="button"
        onClick={() => openModal(event)}
        className="text-left"
      >
        <h3 className="text-[15px] font-semibold leading-snug text-text-primary group-hover:text-primary">
          {event.title}
        </h3>
      </button>

      {event.summary && (
        <p className="line-clamp-3 text-sm text-text-secondary">{event.summary}</p>
      )}

      {event.why_it_matters && (
        <div className="rounded-xl border border-border/50 bg-surface/40 p-3">
          <p className="label-eyebrow mb-1">Why it matters</p>
          <p className="text-xs leading-relaxed text-text-secondary">
            {event.why_it_matters}
          </p>
        </div>
      )}

      <div className="mt-auto flex flex-col gap-3 pt-1">
        <RelevanceBar tier={event.relevance_tier} />
        <div className="flex items-center justify-between text-xs text-muted">
          <span className="flex items-center gap-1.5">
            {event.sources.length > 1 && (
              <span className="flex items-center gap-1 text-text-secondary">
                <Layers size={12} /> {event.sources.length} sources
              </span>
            )}
            {event.sources.length <= 1 && primary && (
              <span className="text-text-secondary">{primary.source_name}</span>
            )}
            {primary?.published_at && <span>· {relativeTime(primary.published_at)}</span>}
          </span>
        </div>
        <div className="flex items-center gap-2">
          {primary && (
            <a
              href={primary.url}
              target="_blank"
              rel="noreferrer"
              className="chip hover:border-primary/40 hover:text-primary"
            >
              <ExternalLink size={12} /> Read source
            </a>
          )}
          <button
            type="button"
            onClick={() => openDock({ event, question: `Explain: ${event.title}` })}
            className="chip hover:border-primary/40 hover:text-primary"
          >
            <MessageSquare size={12} /> Ask AOEN
          </button>
        </div>
      </div>
    </motion.article>
  );
}
