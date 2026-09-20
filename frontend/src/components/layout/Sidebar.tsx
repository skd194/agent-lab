// Primary navigation (§18). Grouped into COMMAND and SETTINGS.

import {
  LayoutDashboard,
  Mic,
  Settings2,
  Wallet,
  type LucideIcon,
} from "lucide-react";
import { NavLink } from "react-router-dom";
import { AICore } from "@/components/core/AICore";
import { domainMeta } from "@/lib/domains";
import { cn } from "@/lib/cn";
import { useAICore } from "@/stores/aiCore";

interface NavItem {
  to: string;
  label: string;
  icon: LucideIcon;
}

const COMMAND: NavItem[] = [
  { to: "/", label: "Overview", icon: LayoutDashboard },
  { to: "/finance", label: domainMeta("finance").short, icon: domainMeta("finance").icon },
  { to: "/technology", label: domainMeta("technology").short, icon: domainMeta("technology").icon },
  { to: "/international", label: domainMeta("international").short, icon: domainMeta("international").icon },
  { to: "/india", label: domainMeta("india").short, icon: domainMeta("india").icon },
  { to: "/science", label: domainMeta("science").short, icon: domainMeta("science").icon },
  { to: "/sports", label: domainMeta("sports").short, icon: domainMeta("sports").icon },
];

const SETTINGS: NavItem[] = [
  { to: "/portfolio", label: "Portfolio", icon: Wallet },
  { to: "/voice", label: "Voice", icon: Mic },
  { to: "/preferences", label: "Preferences", icon: Settings2 },
];

function NavGroup({ title, items }: { title: string; items: NavItem[] }) {
  return (
    <div className="space-y-1">
      <p className="label-eyebrow px-3 pb-1">{title}</p>
      {items.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          end={item.to === "/"}
          className={({ isActive }) =>
            cn(
              "group flex items-center gap-3 rounded-xl px-3 py-2 text-sm transition-colors duration-250",
              isActive
                ? "bg-primary/10 text-text-primary shadow-glow"
                : "text-text-secondary hover:bg-surface/60 hover:text-text-primary",
            )
          }
        >
          {({ isActive }) => (
            <>
              <item.icon
                size={18}
                className={cn(isActive ? "text-primary" : "text-muted group-hover:text-primary")}
              />
              <span className="font-medium">{item.label}</span>
              {isActive && (
                <span className="ml-auto h-1.5 w-1.5 rounded-full bg-primary shadow-glow" />
              )}
            </>
          )}
        </NavLink>
      ))}
    </div>
  );
}

export function Sidebar() {
  const state = useAICore((s) => s.state);
  return (
    <aside className="hidden lg:flex w-64 shrink-0 flex-col gap-6 border-r border-border/60 bg-surface/30 px-4 py-5 backdrop-blur-glass">
      <div className="flex items-center gap-3 px-2">
        <AICore state={state} size={44} />
        <div className="leading-tight">
          <p className="text-lg font-bold tracking-[0.24em] text-text-primary">AOEN</p>
          <p className="text-[10px] uppercase tracking-[0.2em] text-muted">
            Intelligence System
          </p>
        </div>
      </div>

      <nav className="flex flex-1 flex-col gap-6 overflow-y-auto">
        <NavGroup title="Command" items={COMMAND} />
        <NavGroup title="Settings" items={SETTINGS} />
      </nav>

      <p className="px-3 text-[10px] leading-relaxed text-muted">
        Informational only. AOEN does not provide investment advice.
      </p>
    </aside>
  );
}
