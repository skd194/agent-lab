// Global AI-core + voice state (§19, §20). Drives the animated core and the
// voice UI. Kept small and framework-agnostic via zustand.

import { create } from "zustand";
import type { AICoreState } from "@/types";

interface AICoreStore {
  state: AICoreState;
  transcript: string;
  lastResponse: string;
  micActive: boolean;
  setState: (s: AICoreState) => void;
  setTranscript: (t: string) => void;
  setResponse: (r: string) => void;
  setMicActive: (active: boolean) => void;
  reset: () => void;
}

export const useAICore = create<AICoreStore>((set) => ({
  state: "idle",
  transcript: "",
  lastResponse: "",
  micActive: false,
  setState: (state) => set({ state }),
  setTranscript: (transcript) => set({ transcript }),
  setResponse: (lastResponse) => set({ lastResponse }),
  setMicActive: (micActive) => set({ micActive }),
  reset: () => set({ state: "idle", transcript: "", micActive: false }),
}));
