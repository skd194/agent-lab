// Main application layout (§18). Sidebar + top bar + routed content + mobile nav,
// with a global voice overlay and the persistent Ask AOEN dock.

import { useState } from "react";
import { Outlet } from "react-router-dom";
import { AskAoenDock } from "@/components/chat/AskAoenDock";
import { MobileNav } from "@/components/layout/MobileNav";
import { Sidebar } from "@/components/layout/Sidebar";
import { TopBar } from "@/components/layout/TopBar";
import { EventModal } from "@/components/news/EventModal";
import { VoiceOverlay } from "@/components/voice/VoiceOverlay";

export function AppShell() {
  const [voiceOpen, setVoiceOpen] = useState(false);

  return (
    <div className="flex h-full w-full overflow-hidden">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <TopBar onVoice={() => setVoiceOpen(true)} />
        <main className="flex-1 overflow-y-auto px-4 pb-24 pt-6 lg:px-8 lg:pb-10">
          <div className="mx-auto w-full max-w-6xl">
            <Outlet />
          </div>
        </main>
      </div>

      <MobileNav />
      <AskAoenDock />
      <EventModal />
      <VoiceOverlay open={voiceOpen} onClose={() => setVoiceOpen(false)} />
    </div>
  );
}
