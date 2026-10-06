from collections.abc import Sequence

from auction_lens.domain.location import TransitProximity
from auction_lens.domain.market import MarketComparison
from auction_lens.domain.profit import ProfitAnalysis
from auction_lens.domain.report import ListingReport
from auction_lens.domain.rights import RightsAnalysis
from auction_lens.ports import AnalysisRepository


class ReportService:
    """분석 결과를 종합 리포트로 묶고 점수를 매긴다."""

    def __init__(self, repository: AnalysisRepository) -> None:
        self._repository = repository

    def score(
        self,
        rights: RightsAnalysis | None,
        market: MarketComparison | None,
        transit: TransitProximity | None,
        profit: ProfitAnalysis | None,
    ) -> int | None:
        """권리 안전성, 가격 매력, 입지, 수익률을 합친 0~100 점수.

        권리분석이나 시세가 없으면 점수를 내지 않는다.
        """
        raise NotImplementedError

    def build(self, listing_id: str) -> ListingReport:
        """가장 최근에 저장된 리포트를 돌려준다. 없으면 LookupError."""
        raise NotImplementedError

    def rank(self, reports: Sequence[ListingReport]) -> list[ListingReport]:
        """점수 높은 순으로 정렬한다. 점수가 없는 리포트는 맨 뒤."""
        raise NotImplementedError
