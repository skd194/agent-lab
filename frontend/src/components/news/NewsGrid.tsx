// Responsive grid of intelligence cards.

import { NewsCard } from "@/components/news/NewsCard";
import { EmptyState } from "@/components/ui/States";
import type { EventOut } from "@/types";

export function NewsGrid({
  events,
  emptyMessage = "Nothing notable in this window.",
}: {
  events: EventOut[];
  emptyMessage?: string;
}) {
  if (events.length === 0) return <EmptyState message={emptyMessage} />;
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {events.map((event, i) => (
        <NewsCard key={event.id ?? `${event.title}-${i}`} event={event} index={i} />
      ))}
    </div>
  );
}
