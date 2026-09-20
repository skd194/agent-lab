// Persistent Ask AOEN command interface (§23). Answers using retrieved news
// context; when a story is referenced it shows clickable sources.

import { AnimatePresence, motion } from "framer-motion";
import { ExternalLink, MessageSquare, Send, Sparkles, X } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { api } from "@/services/api";
import { cn } from "@/lib/cn";
import { useAssistant } from "@/stores/ui";
import type { ArticleOut, ChatMessage } from "@/types";

interface Turn extends ChatMessage {
  sources?: ArticleOut[];
}

export function AskAoenDock() {
  const { open, contextEvent, seedQuestion, openDock, closeDock } = useAssistant();
  const [input, setInput] = useState("");
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);
  const scrollRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (open && seedQuestion) setInput(seedQuestion);
  }, [open, seedQuestion]);

  useEffect(() => {
    scrollRef.current?.scrollTo({ top: scrollRef.current.scrollHeight });
  }, [turns, busy]);

  const send = async () => {
    const message = input.trim();
    if (!message || busy) return;
    setInput("");
    setTurns((t) => [...t, { role: "user", content: message }]);
    setBusy(true);
    try {
      const res = await api.chat(message, contextEvent?.id ?? undefined);
      setTurns((t) => [
        ...t,
        { role: "assistant", content: res.answer, sources: res.sources },
      ]);
    } catch {
      setTurns((t) => [
        ...t,
        { role: "assistant", content: "I couldn't reach my intelligence core just now." },
      ]);
    } finally {
      setBusy(false);
    }
  };

  return (
    <>
      {!open && (
        <button
          type="button"
          onClick={() => openDock()}
          className="fixed bottom-20 right-4 z-40 flex items-center gap-2 rounded-pill border border-primary/40 bg-surface/80 px-4 py-3 text-sm font-medium text-primary shadow-glow backdrop-blur-glass hover:bg-primary/10 focus-ring lg:bottom-6"
        >
          <Sparkles size={16} /> Ask AOEN
        </button>
      )}

      <AnimatePresence>
        {open && (
          <motion.div
            initial={{ opacity: 0, y: 20, scale: 0.98 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.98 }}
            className="glass-elevated fixed bottom-20 right-4 z-50 flex h-[32rem] w-[calc(100vw-2rem)] max-w-md flex-col overflow-hidden lg:bottom-6"
          >
            <div className="flex items-center justify-between border-b border-border/60 p-4">
              <div className="flex items-center gap-2">
                <MessageSquare size={16} className="text-primary" />
                <span className="text-sm font-semibold text-text-primary">Ask AOEN</span>
              </div>
              <button
                type="button"
                onClick={closeDock}
                aria-label="Close"
                className="grid h-7 w-7 place-items-center rounded-full border border-border/70 text-text-secondary hover:text-text-primary focus-ring"
              >
                <X size={14} />
              </button>
            </div>

            {contextEvent && (
              <div className="border-b border-border/60 bg-surface/40 px-4 py-2">
                <p className="label-eyebrow">Context</p>
                <p className="truncate text-xs text-text-secondary">{contextEvent.title}</p>
              </div>
            )}

            <div ref={scrollRef} className="flex-1 space-y-3 overflow-y-auto p-4">
              {turns.length === 0 && (
                <p className="text-sm text-text-secondary">
                  Ask about a story, your portfolio, or what changed today. AOEN
                  answers from retrieved sources — informational only, not advice.
                </p>
              )}
              {turns.map((turn, i) => (
                <div
                  key={i}
                  className={cn("flex", turn.role === "user" ? "justify-end" : "justify-start")}
                >
                  <div
                    className={cn(
                      "max-w-[85%] whitespace-pre-wrap rounded-2xl px-3 py-2 text-sm",
                      turn.role === "user"
                        ? "bg-primary/15 text-text-primary"
                        : "border border-border/60 bg-surface/50 text-text-secondary",
                    )}
                  >
                    {turn.content}
                    {turn.sources && turn.sources.length > 0 && (
                      <div className="mt-2 space-y-1 border-t border-border/50 pt-2">
                        {turn.sources.map((s) => (
                          <a
                            key={s.url}
                            href={s.url}
                            target="_blank"
                            rel="noreferrer"
                            className="flex items-center gap-1 text-xs text-primary hover:underline"
                          >
                            <ExternalLink size={11} /> {s.source_name}
                          </a>
                        ))}
                      </div>
                    )}
                  </div>
                </div>
              ))}
              {busy && (
                <div className="flex justify-start">
                  <div className="rounded-2xl border border-border/60 bg-surface/50 px-3 py-2 text-sm text-muted">
                    AOEN is thinking…
                  </div>
                </div>
              )}
            </div>

            <div className="border-t border-border/60 p-3">
              <div className="flex items-center gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && send()}
                  placeholder="Ask AOEN…"
                  className="flex-1 rounded-xl border border-border/70 bg-surface/60 px-3 py-2 text-sm text-text-primary placeholder:text-muted focus-ring"
                />
                <button
                  type="button"
                  onClick={send}
                  disabled={busy}
                  aria-label="Send"
                  className="grid h-9 w-9 place-items-center rounded-xl border border-primary/40 bg-primary/10 text-primary hover:bg-primary/20 focus-ring disabled:opacity-50"
                >
                  <Send size={16} />
                </button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  );
}
