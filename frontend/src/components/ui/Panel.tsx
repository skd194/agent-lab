// Reusable glass panel with an optional eyebrow/title/action header.

import type { ReactNode } from "react";
import { cn } from "@/lib/cn";

interface PanelProps {
  children: ReactNode;
  className?: string;
  eyebrow?: string;
  title?: ReactNode;
  action?: ReactNode;
  elevated?: boolean;
}

export function Panel({
  children,
  className,
  eyebrow,
  title,
  action,
  elevated,
}: PanelProps) {
  return (
    <section className={cn(elevated ? "glass-elevated" : "glass", "p-5", className)}>
      {(eyebrow || title || action) && (
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            {eyebrow && <p className="label-eyebrow">{eyebrow}</p>}
            {title && (
              <h2 className="mt-1 text-lg font-semibold text-text-primary">{title}</h2>
            )}
          </div>
          {action}
        </div>
      )}
      {children}
    </section>
  );
}
