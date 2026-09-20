// A single-domain news view (§3).

import { NewsGrid } from "@/components/news/NewsGrid";
import { CardSkeletonGrid, ErrorState } from "@/components/ui/States";
import { domainMeta } from "@/lib/domains";
import { useNews } from "@/services/queries";

export function DomainPage({ domain }: { domain: string }) {
  const { data, isLoading, isError, error } = useNews(domain);
  const meta = domainMeta(domain);

  return (
    <div className="space-y-6">
      <header className="flex items-center gap-3">
        <meta.icon size={22} className="text-primary" />
        <div>
          <p className="label-eyebrow">Domain Intelligence</p>
          <h1 className="text-2xl font-bold text-text-primary">{meta.label}</h1>
        </div>
      </header>

      {isLoading && <CardSkeletonGrid count={6} />}
      {isError && <ErrorState message={(error as Error)?.message} />}
      {data && (
        <NewsGrid events={data} emptyMessage={`No ${meta.label} stories in this window.`} />
      )}
    </div>
  );
}
