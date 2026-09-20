// User preferences (§24). Controls domains, briefing window, stories, voice.

import { Check } from "lucide-react";
import { useEffect, useState } from "react";
import { Panel } from "@/components/ui/Panel";
import { Skeleton } from "@/components/ui/States";
import { DOMAIN_META } from "@/lib/domains";
import { cn } from "@/lib/cn";
import { usePreferences, useUpdatePreferences } from "@/services/queries";
import type { Preferences } from "@/types";

const WINDOWS = [6, 12, 24, 48];
const ALL_DOMAINS = Object.keys(DOMAIN_META);

export function PreferencesPage() {
  const { data, isLoading } = usePreferences();
  const update = useUpdatePreferences();
  const [form, setForm] = useState<Preferences | null>(null);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    if (data && !form) setForm(data);
  }, [data, form]);

  if (isLoading || !form) return <Skeleton className="h-96" />;

  const set = <K extends keyof Preferences>(k: K, v: Preferences[K]) =>
    setForm((f) => (f ? { ...f, [k]: v } : f));

  const toggleDomain = (key: string) => {
    const has = form.preferred_domains.includes(key);
    set(
      "preferred_domains",
      has
        ? form.preferred_domains.filter((d) => d !== key)
        : [...form.preferred_domains, key],
    );
  };

  const field =
    "w-full rounded-xl border border-border/70 bg-surface/60 px-3 py-2 text-sm text-text-primary focus-ring";

  return (
    <div className="space-y-6">
      <header className="space-y-1">
        <p className="label-eyebrow">Settings · Preferences</p>
        <h1 className="text-2xl font-bold text-text-primary">Preferences</h1>
      </header>

      <Panel eyebrow="Profile" title="Identity & schedule">
        <div className="grid gap-4 sm:grid-cols-2">
          <label className="space-y-1">
            <span className="label-eyebrow">Name</span>
            <input className={field} value={form.name} onChange={(e) => set("name", e.target.value)} />
          </label>
          <label className="space-y-1">
            <span className="label-eyebrow">Timezone</span>
            <input
              className={field}
              value={form.timezone}
              onChange={(e) => set("timezone", e.target.value)}
            />
          </label>
          <label className="space-y-1">
            <span className="label-eyebrow">Briefing time</span>
            <input
              type="time"
              className={field}
              value={form.briefing_time}
              onChange={(e) => set("briefing_time", e.target.value)}
            />
          </label>
          <label className="space-y-1">
            <span className="label-eyebrow">Stories per domain</span>
            <input
              type="number"
              min={1}
              max={20}
              className={field}
              value={form.stories_per_domain}
              onChange={(e) => set("stories_per_domain", Number(e.target.value))}
            />
          </label>
        </div>
      </Panel>

      <Panel eyebrow="Coverage" title="News window">
        <div className="flex flex-wrap gap-2">
          {WINDOWS.map((w) => (
            <button
              key={w}
              type="button"
              onClick={() => set("news_window_hours", w)}
              className={cn(
                "chip",
                form.news_window_hours === w
                  ? "border-primary/50 bg-primary/10 text-primary"
                  : "hover:border-primary/40",
              )}
            >
              Last {w}h
            </button>
          ))}
        </div>
      </Panel>

      <Panel eyebrow="Domains" title="What matters to you">
        <div className="flex flex-wrap gap-2">
          {ALL_DOMAINS.map((key) => {
            const active = form.preferred_domains.includes(key);
            const meta = DOMAIN_META[key];
            return (
              <button
                key={key}
                type="button"
                onClick={() => toggleDomain(key)}
                className={cn(
                  "chip",
                  active
                    ? "border-primary/50 bg-primary/10 text-primary"
                    : "hover:border-primary/40",
                )}
              >
                <meta.icon size={13} /> {meta.short}
                {active && <Check size={12} />}
              </button>
            );
          })}
        </div>
      </Panel>

      <Panel eyebrow="Voice" title="Voice interaction">
        <label className="flex items-center gap-3">
          <input
            type="checkbox"
            checked={form.voice_enabled}
            onChange={(e) => set("voice_enabled", e.target.checked)}
            className="h-4 w-4 accent-primary"
          />
          <span className="text-sm text-text-secondary">
            Enable voice briefings and commands
          </span>
        </label>
      </Panel>

      <div className="flex items-center gap-3">
        <button
          type="button"
          disabled={update.isPending}
          onClick={() =>
            update.mutate(form, {
              onSuccess: () => {
                setSaved(true);
                setTimeout(() => setSaved(false), 2000);
              },
            })
          }
          className="rounded-xl border border-primary/40 bg-primary/10 px-5 py-2.5 text-sm font-medium text-primary hover:bg-primary/20 focus-ring disabled:opacity-50"
        >
          {update.isPending ? "Saving…" : "Save preferences"}
        </button>
        {saved && (
          <span className="flex items-center gap-1.5 text-sm text-success">
            <Check size={15} /> Saved
          </span>
        )}
      </div>
    </div>
  );
}
