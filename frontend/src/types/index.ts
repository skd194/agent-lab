// AOEN API types — mirror the backend Pydantic contracts (§33).

export type ImpactType = "positive" | "negative" | "neutral" | "mixed" | "watch";
export type RelevanceTier = "high" | "medium" | "low";
export type FinanceTier = "direct_holding" | "sector" | "macro" | "general";
export type Priority = "HIGH" | "MEDIUM" | "LOW";

export interface SystemStatus {
  name: string;
  tagline: string;
  version: string;
  environment: string;
  demo_mode: boolean;
  live_search: boolean;
  live_llm: boolean;
  status: string;
}

export interface ArticleOut {
  id?: string | null;
  title: string;
  url: string;
  source_name: string;
  ai_summary?: string | null;
  published_at?: string | null;
  retrieved_at?: string | null;
  search_query?: string | null;
}

export interface ImpactOut {
  holding_symbol: string;
  impact_type: ImpactType;
  rationale?: string | null;
}

export interface InsightOut {
  what_happened?: string | null;
  ai_analysis?: string | null;
  portfolio_relevance?: string | null;
  finance_tier?: FinanceTier | null;
  impacts: ImpactOut[];
}

export interface EventOut {
  id?: string | null;
  title: string;
  summary?: string | null;
  category: string;
  why_it_matters?: string | null;
  relevance_tier: RelevanceTier;
  entities: string[];
  verified: boolean;
  event_time?: string | null;
  sources: ArticleOut[];
  insight?: InsightOut | null;
}

export interface DomainSection {
  domain: string;
  label: string;
  events: EventOut[];
  total_available: number;
}

export interface TimeWindow {
  start: string;
  end: string;
  label: string;
}

export interface AgentStep {
  agent: string;
  message: string;
  status: string;
  duration_ms?: number | null;
  item_count?: number | null;
}

export interface BriefingStats {
  total_events: number;
  portfolio_events: number;
  domain_counts: Record<string, number>;
}

export interface DailyBriefing {
  id?: string | null;
  greeting: string;
  headline?: string | null;
  generated_at: string;
  last_briefing_at?: string | null;
  window: TimeWindow;
  stats: BriefingStats;
  top_priorities: EventOut[];
  finance: EventOut[];
  sections: DomainSection[];
  activity: AgentStep[];
  provider: string;
  degraded: boolean;
  notice?: string | null;
}

export interface Holding {
  id: string;
  symbol: string;
  name: string;
  exchange: string;
  sector?: string | null;
  quantity: number;
  average_price: number;
  priority: Priority;
  news_monitoring: boolean;
  last_price?: number | null;
  day_change_pct?: number | null;
  invested_value: number;
  current_value: number;
  unrealized_pl: number;
  unrealized_pl_pct: number;
  day_change_value: number;
  news_count: number;
}

export interface PortfolioOverview {
  total_invested: number;
  current_value: number;
  day_change_value: number;
  day_change_pct: number;
  overall_pl: number;
  overall_pl_pct: number;
  base_currency: string;
  holdings_count: number;
}

export interface Portfolio {
  id: string;
  name: string;
  base_currency: string;
  overview: PortfolioOverview;
  holdings: Holding[];
}

export interface HoldingInput {
  symbol: string;
  name: string;
  exchange: string;
  sector?: string | null;
  quantity: number;
  average_price: number;
  priority: Priority;
  news_monitoring: boolean;
}

export interface Preferences {
  name: string;
  timezone: string;
  briefing_time: string;
  news_window_hours: number;
  stories_per_domain: number;
  voice_enabled: boolean;
  preferred_domains: string[];
}

export interface ChatMessage {
  role: "user" | "assistant";
  content: string;
}

export interface ChatResponse {
  answer: string;
  sources: ArticleOut[];
  used_web_search: boolean;
}

export interface VoiceCommandResult {
  intent: string;
  args: Record<string, unknown>;
  spoken_response: string;
}

export type AICoreState =
  | "idle"
  | "listening"
  | "searching"
  | "thinking"
  | "analyzing"
  | "speaking"
  | "error";
