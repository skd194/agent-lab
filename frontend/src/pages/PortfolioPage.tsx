// Portfolio management (§4, §25): add / edit / delete / toggle monitoring.

import { Pencil, Plus, Power, Trash2, X } from "lucide-react";
import { useState } from "react";
import { Panel } from "@/components/ui/Panel";
import { ErrorState, Skeleton } from "@/components/ui/States";
import { currency } from "@/lib/format";
import { cn } from "@/lib/cn";
import {
  useAddHolding,
  useDeleteHolding,
  usePortfolio,
  useUpdateHolding,
} from "@/services/queries";
import type { HoldingInput, Priority } from "@/types";

const EMPTY: HoldingInput = {
  symbol: "",
  name: "",
  exchange: "NSE",
  sector: "",
  quantity: 0,
  average_price: 0,
  priority: "MEDIUM",
  news_monitoring: true,
};

const PRIORITIES: Priority[] = ["HIGH", "MEDIUM", "LOW"];

function HoldingForm({
  initial,
  onSubmit,
  onCancel,
  submitting,
}: {
  initial: HoldingInput;
  onSubmit: (h: HoldingInput) => void;
  onCancel: () => void;
  submitting: boolean;
}) {
  const [form, setForm] = useState<HoldingInput>(initial);
  const set = <K extends keyof HoldingInput>(k: K, v: HoldingInput[K]) =>
    setForm((f) => ({ ...f, [k]: v }));

  const field =
    "w-full rounded-xl border border-border/70 bg-surface/60 px-3 py-2 text-sm text-text-primary placeholder:text-muted focus-ring";

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSubmit(form);
      }}
      className="grid gap-3 sm:grid-cols-2"
    >
      <label className="space-y-1">
        <span className="label-eyebrow">Security name</span>
        <input
          className={field}
          value={form.name}
          onChange={(e) => set("name", e.target.value)}
          placeholder="Tata Steel"
          required
        />
      </label>
      <label className="space-y-1">
        <span className="label-eyebrow">Symbol</span>
        <input
          className={field}
          value={form.symbol}
          onChange={(e) => set("symbol", e.target.value.toUpperCase())}
          placeholder="TATASTEEL"
          required
        />
      </label>
      <label className="space-y-1">
        <span className="label-eyebrow">Exchange</span>
        <input
          className={field}
          value={form.exchange}
          onChange={(e) => set("exchange", e.target.value.toUpperCase())}
        />
      </label>
      <label className="space-y-1">
        <span className="label-eyebrow">Sector</span>
        <input
          className={field}
          value={form.sector ?? ""}
          onChange={(e) => set("sector", e.target.value)}
          placeholder="Steel"
        />
      </label>
      <label className="space-y-1">
        <span className="label-eyebrow">Quantity</span>
        <input
          type="number"
          className={field}
          value={form.quantity}
          onChange={(e) => set("quantity", Number(e.target.value))}
          min={0}
          step="any"
          required
        />
      </label>
      <label className="space-y-1">
        <span className="label-eyebrow">Average price</span>
        <input
          type="number"
          className={field}
          value={form.average_price}
          onChange={(e) => set("average_price", Number(e.target.value))}
          min={0}
          step="any"
          required
        />
      </label>
      <label className="space-y-1">
        <span className="label-eyebrow">Priority</span>
        <select
          className={field}
          value={form.priority}
          onChange={(e) => set("priority", e.target.value as Priority)}
        >
          {PRIORITIES.map((p) => (
            <option key={p} value={p}>
              {p}
            </option>
          ))}
        </select>
      </label>
      <label className="flex items-center gap-2 pt-6">
        <input
          type="checkbox"
          checked={form.news_monitoring}
          onChange={(e) => set("news_monitoring", e.target.checked)}
          className="h-4 w-4 accent-primary"
        />
        <span className="text-sm text-text-secondary">News monitoring</span>
      </label>

      <div className="col-span-full flex gap-2 pt-2">
        <button
          type="submit"
          disabled={submitting}
          className="rounded-xl border border-primary/40 bg-primary/10 px-4 py-2 text-sm font-medium text-primary hover:bg-primary/20 focus-ring disabled:opacity-50"
        >
          {submitting ? "Saving…" : "Save holding"}
        </button>
        <button
          type="button"
          onClick={onCancel}
          className="rounded-xl border border-border/70 px-4 py-2 text-sm text-text-secondary hover:text-text-primary focus-ring"
        >
          Cancel
        </button>
      </div>
    </form>
  );
}

export function PortfolioPage() {
  const { data, isLoading, isError, error } = usePortfolio();
  const add = useAddHolding();
  const update = useUpdateHolding();
  const remove = useDeleteHolding();
  const [adding, setAdding] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      <header className="flex items-center justify-between">
        <div className="space-y-1">
          <p className="label-eyebrow">Settings · Portfolio</p>
          <h1 className="text-2xl font-bold text-text-primary">My Portfolio</h1>
        </div>
        {!adding && (
          <button
            type="button"
            onClick={() => {
              setAdding(true);
              setEditingId(null);
            }}
            className="flex items-center gap-2 rounded-xl border border-primary/40 bg-primary/10 px-4 py-2 text-sm font-medium text-primary hover:bg-primary/20 focus-ring"
          >
            <Plus size={16} /> Add holding
          </button>
        )}
      </header>

      {adding && (
        <Panel eyebrow="Add holding" title="New position">
          <HoldingForm
            initial={EMPTY}
            submitting={add.isPending}
            onCancel={() => setAdding(false)}
            onSubmit={(h) => add.mutate(h, { onSuccess: () => setAdding(false) })}
          />
        </Panel>
      )}

      {isLoading && <Skeleton className="h-40" />}
      {isError && <ErrorState message={(error as Error)?.message} />}

      <div className="space-y-3">
        {data?.holdings.map((h) =>
          editingId === h.id ? (
            <Panel key={h.id} eyebrow="Edit holding" title={h.name}>
              <HoldingForm
                initial={{
                  symbol: h.symbol,
                  name: h.name,
                  exchange: h.exchange,
                  sector: h.sector ?? "",
                  quantity: h.quantity,
                  average_price: h.average_price,
                  priority: h.priority,
                  news_monitoring: h.news_monitoring,
                }}
                submitting={update.isPending}
                onCancel={() => setEditingId(null)}
                onSubmit={(data2) =>
                  update.mutate(
                    { id: h.id, data: data2 },
                    { onSuccess: () => setEditingId(null) },
                  )
                }
              />
            </Panel>
          ) : (
            <div
              key={h.id}
              className="glass flex flex-wrap items-center justify-between gap-3 p-4"
            >
              <div>
                <p className="font-medium text-text-primary">
                  {h.name}{" "}
                  <span className="font-mono text-xs text-muted">
                    {h.symbol} · {h.exchange}
                  </span>
                </p>
                <p className="text-sm text-text-secondary">
                  {h.quantity} @ {currency(h.average_price)} · {h.sector ?? "—"} ·{" "}
                  <span className="text-muted">{h.priority}</span>
                </p>
              </div>
              <div className="flex items-center gap-2">
                <span
                  className={cn(
                    "chip",
                    h.news_monitoring
                      ? "border-success/40 text-success"
                      : "text-muted",
                  )}
                >
                  <Power size={12} /> {h.news_monitoring ? "Monitoring" : "Off"}
                </span>
                <button
                  type="button"
                  aria-label="Edit"
                  onClick={() => {
                    setEditingId(h.id);
                    setAdding(false);
                  }}
                  className="grid h-8 w-8 place-items-center rounded-lg border border-border/70 text-text-secondary hover:text-primary focus-ring"
                >
                  <Pencil size={14} />
                </button>
                <button
                  type="button"
                  aria-label="Delete"
                  onClick={() => remove.mutate(h.id)}
                  className="grid h-8 w-8 place-items-center rounded-lg border border-border/70 text-text-secondary hover:text-danger focus-ring"
                >
                  {remove.isPending ? <X size={14} /> : <Trash2 size={14} />}
                </button>
              </div>
            </div>
          ),
        )}
      </div>
    </div>
  );
}
