// Thin fetch client. All requests hit the FastAPI backend via the Vite proxy,
// so the browser never contacts external services and no keys reach it (§37).

const BASE = "/api";

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!res.ok) {
    const detail = await res.text().catch(() => res.statusText);
    throw new Error(`${res.status}: ${detail}`);
  }
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

import type {
  ChatResponse,
  DailyBriefing,
  EventOut,
  Holding,
  HoldingInput,
  Portfolio,
  Preferences,
  SystemStatus,
  VoiceCommandResult,
} from "@/types";

export const api = {
  systemStatus: () => request<SystemStatus>("/system/status"),

  briefingToday: (windowHours = 24, refresh = false) =>
    request<DailyBriefing>(
      `/briefing/today?window_hours=${windowHours}&refresh=${refresh}`,
    ),

  news: (category?: string) =>
    request<EventOut[]>(`/news${category ? `?category=${category}` : ""}`),
  event: (id: string) => request<EventOut>(`/news/${id}`),

  portfolio: () => request<Portfolio>("/finance/portfolio"),
  financeNews: () => request<EventOut[]>("/finance/news"),
  addHolding: (h: HoldingInput) =>
    request<Holding>("/finance/portfolio", {
      method: "POST",
      body: JSON.stringify(h),
    }),
  updateHolding: (id: string, h: Partial<HoldingInput>) =>
    request<Holding>(`/finance/portfolio/${id}`, {
      method: "PUT",
      body: JSON.stringify(h),
    }),
  deleteHolding: (id: string) =>
    request<void>(`/finance/portfolio/${id}`, { method: "DELETE" }),

  preferences: () => request<Preferences>("/preferences"),
  updatePreferences: (p: Partial<Preferences>) =>
    request<Preferences>("/preferences", {
      method: "PUT",
      body: JSON.stringify(p),
    }),

  chat: (message: string, eventId?: string) =>
    request<ChatResponse>("/ai/chat", {
      method: "POST",
      body: JSON.stringify({ message, event_id: eventId ?? null, history: [] }),
    }),

  voiceCommand: (transcript: string) =>
    request<VoiceCommandResult>("/voice/command", {
      method: "POST",
      body: JSON.stringify({ transcript }),
    }),
};
