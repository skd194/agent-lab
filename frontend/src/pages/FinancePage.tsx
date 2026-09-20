// Finance intelligence dashboard (§6, §7).

import { Link } from "react-router-dom";
import { HoldingsTable } from "@/components/finance/HoldingsTable";
import { PortfolioSummary } from "@/components/finance/PortfolioSummary";
import { NewsGrid } from "@/components/news/NewsGrid";
import { Panel } from "@/components/ui/Panel";
import { CardSkeletonGrid, ErrorState, Skeleton } from "@/components/ui/States";
import { useFinanceNews, usePortfolio } from "@/services/queries";

export function FinancePage() {
  const portfolio = usePortfolio();
  const news = useFinanceNews();

  return (
    <div className="space-y-8">
      <header className="space-y-1">
        <p className="label-eyebrow">Finance Intelligence</p>
        <h1 className="text-2xl font-bold text-text-primary">Portfolio Command</h1>
        <p className="text-sm text-text-secondary">
          Ranked by relevance to your holdings. Informational only — not advice.
        </p>
      </header>

      {portfolio.isLoading && <Skeleton className="h-28" />}
      {portfolio.isError && <ErrorState message={(portfolio.error as Error)?.message} />}
      {portfolio.data && (
        <>
          <PortfolioSummary overview={portfolio.data.overview} />
          <Panel
            eyebrow="Holdings"
            title="Positions"
            action={
              <Link to="/portfolio" className="chip hover:border-primary/40 hover:text-primary">
                Manage
              </Link>
            }
          >
            <HoldingsTable
              holdings={portfolio.data.holdings}
              currencyCode={portfolio.data.base_currency}
            />
          </Panel>
        </>
      )}

      <section className="space-y-4">
        <h2 className="text-base font-semibold uppercase tracking-[0.14em] text-text-primary">
          Finance News
        </h2>
        {news.isLoading && <CardSkeletonGrid count={3} />}
        {news.isError && <ErrorState message={(news.error as Error)?.message} />}
        {news.data && (
          <NewsGrid events={news.data} emptyMessage="No finance news in this window." />
        )}
      </section>
    </div>
  );
}
