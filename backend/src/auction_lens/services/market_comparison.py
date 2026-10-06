from collections.abc import Sequence

from auction_lens.domain.listing import Listing
from auction_lens.domain.market import AskingListing, MarketComparison, TradeRecord
from auction_lens.ports import AskingPriceSource, TradeDataSource


class MarketComparisonService:
    """같은 지역의 실거래·매물과 가격을 비교한다."""

    def __init__(
        self, trades: TradeDataSource, asking: AskingPriceSource | None = None
    ) -> None:
        self._trades = trades
        self._asking = asking

    def fetch_comparables(
        self, listing: Listing, months: int = 12, area_tolerance: float = 0.1
    ) -> list[TradeRecord]:
        """최근 months개월의 같은 종류·유사 면적 실거래를 찾는다.

        같은 단지 → 같은 법정동 순으로 넓히고, 면적은 전용면적 ±area_tolerance 범위.
        """
        raise NotImplementedError

    def fetch_asking_listings(self, listing: Listing) -> list[AskingListing]:
        """현재 나와 있는 유사 매물의 호가. 호가 소스가 없으면 빈 목록."""
        raise NotImplementedError

    def estimate_market_price(
        self, listing: Listing, comparables: Sequence[TradeRecord]
    ) -> int | None:
        """비교 거래로 시세를 추정한다. 표본이 부족하면 None."""
        raise NotImplementedError

    def compare(self, listing: Listing) -> MarketComparison:
        """비교 거래·호가를 모아 추정 시세와 가격 비율을 계산한다."""
        raise NotImplementedError
