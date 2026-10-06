from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from auction_lens.domain.listing import PropertyType


class DealKind(StrEnum):
    SALE = "sale"  # 매매
    JEONSE = "jeonse"  # 전세
    MONTHLY_RENT = "monthly_rent"  # 월세


@dataclass
class TradeRecord:
    """실거래 신고 한 건."""

    property_type: PropertyType
    deal_kind: DealKind
    legal_dong_code: str
    address: str
    deal_date: date
    price: int  # 매매가 또는 보증금
    monthly_rent: int = 0
    building_name: str = ""
    exclusive_area_m2: float | None = None
    floor: int | None = None
    built_year: int | None = None


@dataclass
class AskingListing:
    """시장에 나와 있는 매물(호가)."""

    source: str
    property_type: PropertyType
    deal_kind: DealKind
    asking_price: int
    monthly_rent: int = 0
    building_name: str = ""
    exclusive_area_m2: float | None = None
    floor: int | None = None
    listed_on: date | None = None
    url: str = ""


@dataclass
class MarketComparison:
    listing_id: str
    comparables: list[TradeRecord] = field(default_factory=list)
    asking_listings: list[AskingListing] = field(default_factory=list)
    estimated_price: int | None = None  # 추정 시세
    median_price_per_m2: int | None = None
    median_asking_price: int | None = None
    minimum_bid_ratio: float | None = None  # 최저매각가격 / 추정 시세
    appraisal_ratio: float | None = None  # 감정가 / 추정 시세
    jeonse_ratio: float | None = None  # 전세가율
    period_months: int = 12
    basis: str = ""  # 비교 대상 선정 기준 (같은 단지, 같은 동 등)
