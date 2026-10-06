from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


class RightType(StrEnum):
    MORTGAGE = "mortgage"  # (근)저당권
    PROVISIONAL_SEIZURE = "provisional_seizure"  # 가압류
    SEIZURE = "seizure"  # 압류
    SECURITY_PROVISIONAL_REGISTRATION = "security_provisional_registration"  # 담보가등기
    OWNERSHIP_PROVISIONAL_REGISTRATION = "ownership_provisional_registration"  # 소유권이전청구권 가등기
    AUCTION_COMMENCEMENT = "auction_commencement"  # 경매개시결정등기
    JEONSE = "jeonse"  # 전세권
    LEASE_REGISTRATION = "lease_registration"  # 임차권등기
    SUPERFICIES = "superficies"  # 지상권
    EASEMENT = "easement"  # 지역권
    PROVISIONAL_DISPOSITION = "provisional_disposition"  # 가처분
    REPURCHASE = "repurchase"  # 환매등기
    OTHER = "other"


class Disposition(StrEnum):
    EXTINGUISHED = "extinguished"  # 소멸
    ASSUMED = "assumed"  # 낙찰자 인수
    UNCERTAIN = "uncertain"  # 판정 불가, 사람이 확인


class RiskFlag(StrEnum):
    LIEN = "lien"  # 유치권 신고
    STATUTORY_SUPERFICIES = "statutory_superficies"  # 법정지상권 성립 여지
    GRAVE_RIGHT = "grave_right"  # 분묘기지권
    SHARE_SALE = "share_sale"  # 지분 매각
    LAND_RIGHT_UNREGISTERED = "land_right_unregistered"  # 대지권 미등기
    SEPARATE_LAND_REGISTRATION = "separate_land_registration"  # 토지 별도등기
    ILLEGAL_BUILDING = "illegal_building"  # 위반건축물
    SENIOR_TENANT = "senior_tenant"  # 대항력 있는 선순위 임차인
    ASSUMED_RIGHT = "assumed_right"  # 인수되는 등기 권리 존재
    FARMLAND_QUALIFICATION = "farmland_qualification"  # 농지취득자격증명 필요
    NO_REGISTRY = "no_registry"  # 등기사항증명서 없이 분석함
    NO_EVICTION_ORDER = "no_eviction_order"  # 공매: 인도명령 불가


@dataclass
class RegistryRight:
    """등기부에 기재된 권리 한 건."""

    type: RightType
    holder: str
    registered_on: date  # 접수일
    amount: int | None = None  # 채권최고액, 청구금액, 전세금
    section: str = ""  # "갑구" 또는 "을구"
    rank_no: str = ""  # 순위번호
    demanded_distribution: bool = False  # 전세권자가 배당요구했거나 경매를 신청함
    note: str = ""


@dataclass
class Tenant:
    name: str
    move_in_date: date | None  # 전입신고일
    fixed_date: date | None  # 확정일자
    deposit: int | None
    monthly_rent: int = 0
    demanded_distribution: bool = False  # 배당요구 종기 내 배당요구 여부
    occupied_part: str = ""
    note: str = ""


@dataclass
class RightsInput:
    """권리분석 입력. 문서 파싱 결과를 합쳐 만든다."""

    listing_id: str
    rights: list[RegistryRight] = field(default_factory=list)
    tenants: list[Tenant] = field(default_factory=list)
    remarks: list[str] = field(default_factory=list)  # 매각물건명세서 비고 등 특이사항 원문
    distribution_demand_deadline: date | None = None  # 배당요구 종기
    has_registry: bool = False  # 등기사항증명서를 근거로 했는지


@dataclass
class RightJudgement:
    right: RegistryRight
    disposition: Disposition
    reason: str


@dataclass
class TenantJudgement:
    tenant: Tenant
    has_opposing_power: bool | None  # 대항력. None은 판정 불가
    has_priority_repayment: bool | None  # 우선변제권
    expected_distribution: int  # 예상 배당액
    assumed_deposit: int  # 낙찰자가 인수하는 보증금
    reason: str


@dataclass
class DistributionEntry:
    rank: int
    creditor: str
    kind: str  # 집행비용, 최우선변제, 당해세, 근저당 등
    claim: int
    amount: int  # 실제 배당액


@dataclass
class RightsAnalysis:
    listing_id: str
    baseline_right: RegistryRight | None  # 말소기준권리
    right_judgements: list[RightJudgement] = field(default_factory=list)
    tenant_judgements: list[TenantJudgement] = field(default_factory=list)
    distribution: list[DistributionEntry] = field(default_factory=list)
    assumed_amount: int = 0  # 인수금액 합계 (등기 권리 + 임차 보증금)
    risk_flags: list[RiskFlag] = field(default_factory=list)
    summary: str = ""
    rules_version: str = ""  # 적용한 rules/ 기준 버전
