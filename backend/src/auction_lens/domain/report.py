from dataclasses import dataclass, field
from datetime import datetime

from auction_lens.domain.document import Document
from auction_lens.domain.listing import Listing
from auction_lens.domain.location import TransitProximity
from auction_lens.domain.market import MarketComparison
from auction_lens.domain.profit import ProfitAnalysis
from auction_lens.domain.rights import RightsAnalysis


@dataclass
class StepFailure:
    step: str
    reason: str


@dataclass
class ListingReport:
    """물건 한 건의 종합 분석 결과. 실패한 단계는 None으로 두고 failures에 사유를 남긴다."""

    listing: Listing
    generated_at: datetime
    documents: list[Document] = field(default_factory=list)
    rights: RightsAnalysis | None = None
    market: MarketComparison | None = None
    transit: TransitProximity | None = None
    profit: ProfitAnalysis | None = None
    score: int | None = None  # 0~100
    failures: list[StepFailure] = field(default_factory=list)
