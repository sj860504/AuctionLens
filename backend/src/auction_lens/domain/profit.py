from dataclasses import dataclass, field


@dataclass(frozen=True)
class ProfitAssumptions:
    """수익 계산에 쓰는 가정. 사용자가 바꿀 수 있는 값."""

    bid_price: int  # 입찰(낙찰) 가격
    expected_sale_price: int | None = None  # 매도 예상가. None이면 추정 시세 사용
    holding_months: int = 12
    loan_ltv: float = 0.0  # 낙찰가 대비 경락잔금대출 비율
    loan_rate: float = 0.0  # 연 이자율
    repair_cost: int = 0
    eviction_cost: int = 0  # 명도비
    unpaid_maintenance_fee: int = 0  # 인수할 체납 관리비
    legal_fee: int | None = None  # 법무비. None이면 기준표로 추정
    brokerage_fee: int | None = None  # 매도 중개보수. None이면 기준표로 추정
    owned_house_count: int = 0  # 취득 전 보유 주택 수 (취득세 중과 판단)
    monthly_rent: int = 0  # 보유 중 임대 시 월세
    rent_deposit: int = 0


@dataclass
class AcquisitionCost:
    bid_price: int
    acquisition_tax: int  # 취득세 + 지방교육세 + 농어촌특별세
    legal_fee: int
    assumed_amount: int  # 권리분석 인수금액
    eviction_cost: int
    repair_cost: int
    unpaid_maintenance_fee: int

    @property
    def total(self) -> int:
        return (
            self.bid_price
            + self.acquisition_tax
            + self.legal_fee
            + self.assumed_amount
            + self.eviction_cost
            + self.repair_cost
            + self.unpaid_maintenance_fee
        )


@dataclass
class ProfitScenario:
    name: str  # 보수, 기준, 낙관
    assumptions: ProfitAssumptions
    acquisition_cost: AcquisitionCost
    loan_amount: int
    equity: int  # 실투자금 = 총 취득 비용 - 대출 - 임대 보증금
    interest_cost: int  # 보유 기간 이자
    sale_price: int
    capital_gains_tax: int
    net_profit: int  # 세후 순이익
    roi: float  # 실투자금 대비 수익률
    annualized_roi: float
    rental_yield: float | None = None  # 임대 시 연 수익률


@dataclass
class ProfitAnalysis:
    listing_id: str
    scenarios: list[ProfitScenario] = field(default_factory=list)
    break_even_bid: int | None = None  # 순이익 0이 되는 입찰가
    max_bid_price: int | None = None  # 목표 수익률을 만족하는 입찰 상한가
    target_roi: float | None = None
    rules_version: str = ""  # 적용한 세율 기준 버전
