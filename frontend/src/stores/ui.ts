// UI stores: event detail modal + Ask AOEN dock context.

import { create } from "zustand";
import type { EventOut } from "@/types";

interface EventModalStore {
  event: EventOut | null;
  open: (event: EventOut) => void;
  close: () => void;
}

export const useEventModal = create<EventModalStore>((set) => ({
  event: null,
  open: (event) => set({ event }),
  close: () => set({ event: null }),
}));

interface AssistantStore {
  open: boolean;
  contextEvent: EventOut | null;
  seedQuestion: string;
  openDock: (opts?: { event?: EventOut; question?: string }) => void;
  closeDock: () => void;
}

export const useAssistant = create<AssistantStore>((set) => ({
  open: false,
  contextEvent: null,
  seedQuestion: "",
  openDock: (opts) =>
    set({
      open: true,
      contextEvent: opts?.event ?? null,
      seedQuestion: opts?.question ?? "",
    }),
  closeDock: () => set({ open: false, seedQuestion: "" }),
}));
