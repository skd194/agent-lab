// Loading skeletons and error/empty states (§39: never a blank dashboard).

import { AlertTriangle, Inbox } from "lucide-react";
import { cn } from "@/lib/cn";

export function Skeleton({ className }: { className?: string }) {
  return (
    <div
      className={cn(
        "relative overflow-hidden rounded-xl bg-surface/60",
        "after:absolute after:inset-0 after:-translate-x-full after:animate-shimmer",
        "after:bg-gradient-to-r after:from-transparent after:via-white/5 after:to-transparent",
        className,
      )}
    />
  );
}

export function CardSkeletonGrid({ count = 3 }: { count?: number }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-3">
      {Array.from({ length: count }).map((_, i) => (
        <Skeleton key={i} className="h-44" />
      ))}
    </div>
  );
}

export function ErrorState({ message }: { message?: string }) {
  return (
    <div className="glass flex flex-col items-center gap-3 p-8 text-center">
      <AlertTriangle className="text-warning" size={28} />
      <p className="font-semibold text-text-primary">News update delayed</p>
      <p className="max-w-sm text-sm text-text-secondary">
        {message ??
          "Some sources are temporarily unavailable. Showing the latest verified information available."}
      </p>
    </div>
  );
}

export function EmptyState({ message }: { message: string }) {
  return (
    <div className="glass flex flex-col items-center gap-3 p-8 text-center text-text-secondary">
      <Inbox size={26} className="text-muted" />
      <p className="text-sm">{message}</p>
    </div>
  );
}
