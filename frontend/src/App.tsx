import { createBrowserRouter } from "react-router-dom";
import { AppShell } from "@/layouts/AppShell";
import { DomainPage } from "@/pages/DomainPage";
import { FinancePage } from "@/pages/FinancePage";
import { NewsPage } from "@/pages/NewsPage";
import { OverviewPage } from "@/pages/OverviewPage";
import { PortfolioPage } from "@/pages/PortfolioPage";
import { PreferencesPage } from "@/pages/PreferencesPage";
import { VoicePage } from "@/pages/VoicePage";

export const router = createBrowserRouter([
  {
    path: "/",
    element: <AppShell />,
    children: [
      { index: true, element: <OverviewPage /> },
      { path: "finance", element: <FinancePage /> },
      { path: "technology", element: <DomainPage domain="technology" /> },
      { path: "international", element: <DomainPage domain="international" /> },
      { path: "india", element: <DomainPage domain="india" /> },
      { path: "science", element: <DomainPage domain="science" /> },
      { path: "sports", element: <DomainPage domain="sports" /> },
      { path: "news", element: <NewsPage /> },
      { path: "portfolio", element: <PortfolioPage /> },
      { path: "voice", element: <VoicePage /> },
      { path: "preferences", element: <PreferencesPage /> },
    ],
  },
]);
