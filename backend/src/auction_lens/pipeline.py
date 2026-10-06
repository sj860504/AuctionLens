from auction_lens.domain.listing import SearchCriteria
from auction_lens.domain.profit import ProfitAssumptions
from auction_lens.domain.report import ListingReport
from auction_lens.ports import AnalysisRepository
from auction_lens.services.document_collection import DocumentCollectionService
from auction_lens.services.listing_search import ListingSearchService
from auction_lens.services.market_comparison import MarketComparisonService
from auction_lens.services.report import ReportService
from auction_lens.services.transit_proximity import TransitProximityService


class AnalysisPipeline:
    """수집 → 파싱 → 권리분석 → 시세 → 역세권 → 수익성 → 리포트 순으로 실행한다."""

    def __init__(
        self,
        search: ListingSearchService,
        documents: DocumentCollectionService,
        market: MarketComparisonService,
        transit: TransitProximityService,
        reports: ReportService,
        repository: AnalysisRepository,
    ) -> None:
        self._search = search
        self._documents = documents
        self._market = market
        self._transit = transit
        self._reports = reports
        self._repository = repository

    def run(self, listing_id: str, assumptions: ProfitAssumptions | None = None) -> ListingReport:
        """물건 한 건을 끝까지 분석해 저장한다.

        한 단계가 실패해도 나머지는 계속하고 ListingReport.failures에 사유를 남긴다.
        assumptions가 없으면 최저매각가격을 입찰가로 가정한다.
        """
        raise NotImplementedError

    def run_search(
        self, criteria: SearchCriteria, assumptions: ProfitAssumptions | None = None
    ) -> list[ListingReport]:
        """검색 결과 전체를 분석해 점수순으로 돌려준다."""
        raise NotImplementedError
