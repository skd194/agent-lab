// A briefing domain section (§3, §12): header with count + expandable grid.

import { ChevronDown } from "lucide-react";
import { useState } from "react";
import { NewsGrid } from "@/components/news/NewsGrid";
import { domainMeta } from "@/lib/domains";
import { cn } from "@/lib/cn";
import type { DomainSection } from "@/types";

export function DomainSectionBlock({ section }: { section: DomainSection }) {
  const [expanded, setExpanded] = useState(false);
  const meta = domainMeta(section.domain);
  const shown = expanded ? section.events : section.events.slice(0, 3);
  const canExpand = section.events.length > 3;

  return (
    <section className="space-y-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2.5">
          <meta.icon size={18} className="text-primary" />
          <h2 className="text-base font-semibold uppercase tracking-[0.14em] text-text-primary">
            {meta.label}
          </h2>
          <span className="chip">{section.events.length} stories</span>
        </div>
        {canExpand && (
          <button
            type="button"
            onClick={() => setExpanded((v) => !v)}
            className="chip hover:border-primary/40 hover:text-primary"
          >
            {expanded ? "Show less" : "Expand"}
            <ChevronDown
              size={13}
              className={cn("transition-transform", expanded && "rotate-180")}
            />
          </button>
        )}
      </div>
      <NewsGrid events={shown} />
    </section>
  );
}
