// React Query hooks (§29 background refresh, cached briefing shown immediately).

import {
  useMutation,
  useQuery,
  useQueryClient,
} from "@tanstack/react-query";
import { api } from "@/services/api";
import type { HoldingInput, Preferences } from "@/types";

export const keys = {
  status: ["system", "status"] as const,
  briefing: (w: number) => ["briefing", w] as const,
  portfolio: ["finance", "portfolio"] as const,
  financeNews: ["finance", "news"] as const,
  preferences: ["preferences"] as const,
  news: (c?: string) => ["news", c ?? "all"] as const,
};

export function useSystemStatus() {
  return useQuery({ queryKey: keys.status, queryFn: api.systemStatus });
}

export function useBriefing(windowHours = 24) {
  return useQuery({
    queryKey: keys.briefing(windowHours),
    queryFn: () => api.briefingToday(windowHours),
    staleTime: 5 * 60 * 1000,
  });
}

export function usePortfolio() {
  return useQuery({ queryKey: keys.portfolio, queryFn: api.portfolio });
}

export function useFinanceNews() {
  return useQuery({ queryKey: keys.financeNews, queryFn: api.financeNews });
}

export function usePreferences() {
  return useQuery({ queryKey: keys.preferences, queryFn: api.preferences });
}

export function useNews(category?: string) {
  return useQuery({
    queryKey: keys.news(category),
    queryFn: () => api.news(category),
  });
}

export function useAddHolding() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (h: HoldingInput) => api.addHolding(h),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.portfolio }),
  });
}

export function useUpdateHolding() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: ({ id, data }: { id: string; data: Partial<HoldingInput> }) =>
      api.updateHolding(id, data),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.portfolio }),
  });
}

export function useDeleteHolding() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (id: string) => api.deleteHolding(id),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.portfolio }),
  });
}

export function useUpdatePreferences() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: (p: Partial<Preferences>) => api.updatePreferences(p),
    onSuccess: () => qc.invalidateQueries({ queryKey: keys.preferences }),
  });
}
