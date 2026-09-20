// Bottom mobile navigation (§40). Home / Finance / News / AOEN / Settings.

import { Home, LineChart, Mic, Newspaper, Settings2 } from "lucide-react";
import { NavLink } from "react-router-dom";
import { cn } from "@/lib/cn";

const ITEMS = [
  { to: "/", label: "Home", icon: Home, end: true },
  { to: "/finance", label: "Finance", icon: LineChart, end: false },
  { to: "/news", label: "News", icon: Newspaper, end: false },
  { to: "/voice", label: "AOEN", icon: Mic, end: false },
  { to: "/preferences", label: "Settings", icon: Settings2, end: false },
];

export function MobileNav() {
  return (
    <nav className="fixed inset-x-0 bottom-0 z-40 flex items-stretch justify-around border-t border-border/60 bg-surface/80 backdrop-blur-glass lg:hidden">
      {ITEMS.map((item) => (
        <NavLink
          key={item.to}
          to={item.to}
          end={item.end}
          className={({ isActive }) =>
            cn(
              "flex flex-1 flex-col items-center gap-1 py-2 text-[10px] font-medium transition-colors",
              isActive ? "text-primary" : "text-muted",
            )
          }
        >
          <item.icon size={20} />
          {item.label}
        </NavLink>
      ))}
    </nav>
  );
}
