// All news with a category filter (§13). Used by mobile nav.

import { useState } from "react";
import { NewsGrid } from "@/components/news/NewsGrid";
import { CardSkeletonGrid, ErrorState } from "@/components/ui/States";
import { DOMAIN_META } from "@/lib/domains";
import { cn } from "@/lib/cn";
import { useNews } from "@/services/queries";

const FILTERS = ["all", "finance", "technology", "international", "india", "science", "sports"];

export function NewsPage() {
  const [filter, setFilter] = useState("all");
  const { data, isLoading, isError, error } = useNews(
    filter === "all" ? undefined : filter,
  );

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <p className="label-eyebrow">World Intelligence</p>
        <h1 className="text-2xl font-bold text-text-primary">News</h1>
      </header>

      <div className="flex flex-wrap gap-2">
        {FILTERS.map((f) => (
          <button
            key={f}
            type="button"
            onClick={() => setFilter(f)}
            className={cn(
              "chip capitalize transition-colors",
              filter === f
                ? "border-primary/50 bg-primary/10 text-primary"
                : "hover:border-primary/40 hover:text-primary",
            )}
          >
            {f === "all" ? "All" : DOMAIN_META[f]?.short ?? f}
          </button>
        ))}
      </div>

      {isLoading && <CardSkeletonGrid count={6} />}
      {isError && <ErrorState message={(error as Error)?.message} />}
      {data && <NewsGrid events={data} />}
    </div>
  );
}
