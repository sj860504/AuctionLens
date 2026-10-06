from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum

from auction_lens.domain.location import Coordinate


class SaleType(StrEnum):
    COURT_AUCTION = "court_auction"  # 법원 경매
    PUBLIC_SALE = "public_sale"  # 공매 (온비드)


class PropertyType(StrEnum):
    APARTMENT = "apartment"  # 아파트
    MULTI_FAMILY = "multi_family"  # 연립·다세대
    HOUSE = "house"  # 단독·다가구
    OFFICETEL = "officetel"
    COMMERCIAL = "commercial"  # 상가·업무시설
    LAND = "land"
    OTHER = "other"


class ListingStatus(StrEnum):
    SCHEDULED = "scheduled"  # 입찰 예정
    FAILED = "failed"  # 유찰
    SOLD = "sold"  # 매각(낙찰)
    CANCELLED = "cancelled"  # 취하·취소·변경
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class SearchCriteria:
    sale_types: tuple[SaleType, ...] = (SaleType.COURT_AUCTION, SaleType.PUBLIC_SALE)
    legal_dong_codes: tuple[str, ...] = ()  # 법정동 코드 앞자리 (시군구 5자리 이상)
    property_types: tuple[PropertyType, ...] = ()
    min_price: int | None = None  # 최저매각가격 기준
    max_price: int | None = None
    min_failed_count: int = 0
    bid_date_from: date | None = None
    bid_date_to: date | None = None


@dataclass
class Listing:
    """경매·공매 물건 한 건. 소스별 응답을 이 모델로 정규화한다."""

    id: str  # "{source}:{사건번호 또는 물건관리번호}:{물건번호}"
    source: str  # 어댑터 이름
    sale_type: SaleType
    case_number: str  # 사건번호(경매) 또는 물건관리번호(공매)
    property_type: PropertyType
    address: str
    appraised_price: int  # 감정가
    minimum_bid_price: int  # 최저매각가격
    item_number: int = 1  # 물건번호
    agency: str = ""  # 관할 법원 또는 공매 집행기관
    legal_dong_code: str = ""  # 법정동 코드 10자리
    building_name: str = ""  # 단지·건물명
    exclusive_area_m2: float | None = None  # 전용면적
    land_area_m2: float | None = None  # 대지(지분) 면적
    floor: int | None = None
    built_year: int | None = None
    failed_count: int = 0  # 유찰 횟수
    bid_date: date | None = None  # 매각(입찰) 기일
    status: ListingStatus = ListingStatus.UNKNOWN
    coordinate: Coordinate | None = None
    source_url: str = ""
    remarks: list[str] = field(default_factory=list)  # 목록에 표시된 특이사항

    @property
    def bid_deposit(self) -> int:
        """입찰보증금. 통상 최저매각가격의 10%."""
        return self.minimum_bid_price // 10
