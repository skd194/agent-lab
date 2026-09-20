// Daily Briefing — the primary screen (§12).

import { Star } from "lucide-react";
import { ActivityPanel } from "@/components/briefing/ActivityPanel";
import { BriefingHero } from "@/components/briefing/BriefingHero";
import { DomainSectionBlock } from "@/components/briefing/DomainSectionBlock";
import { NewsGrid } from "@/components/news/NewsGrid";
import { domainMeta } from "@/lib/domains";
import { CardSkeletonGrid, ErrorState, Skeleton } from "@/components/ui/States";
import { useBriefing } from "@/services/queries";

export function OverviewPage() {
  const { data, isLoading, isError, error } = useBriefing(24);

  if (isLoading) {
    return (
      <div className="space-y-6">
        <Skeleton className="h-56" />
        <CardSkeletonGrid count={3} />
      </div>
    );
  }
  if (isError || !data) {
    return <ErrorState message={(error as Error)?.message} />;
  }

  const financeMeta = domainMeta("finance");

  return (
    <div className="space-y-8">
      <BriefingHero briefing={data} />

      <ActivityPanel steps={data.activity} />

      {data.top_priorities.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-2.5">
            <Star size={18} className="text-warning" />
            <h2 className="text-base font-semibold uppercase tracking-[0.14em] text-text-primary">
              Top Priorities
            </h2>
          </div>
          <NewsGrid events={data.top_priorities} />
        </section>
      )}

      {data.finance.length > 0 && (
        <section className="space-y-4">
          <div className="flex items-center gap-2.5">
            <financeMeta.icon size={18} className="text-primary" />
            <h2 className="text-base font-semibold uppercase tracking-[0.14em] text-text-primary">
              Your Finance
            </h2>
            <span className="chip">{data.finance.length} stories</span>
          </div>
          <NewsGrid events={data.finance} />
        </section>
      )}

      {data.sections.map((section) => (
        <DomainSectionBlock key={section.domain} section={section} />
      ))}
    </div>
  );
}
