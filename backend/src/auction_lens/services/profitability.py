"""수익성 분석. 세율·기준표는 rules/에서 읽고, 계산은 순수 함수로 둔다."""

from auction_lens.domain.listing import Listing, PropertyType
from auction_lens.domain.market import MarketComparison
from auction_lens.domain.profit import (
    AcquisitionCost,
    ProfitAnalysis,
    ProfitAssumptions,
    ProfitScenario,
)
from auction_lens.domain.rights import RightsAnalysis


def calc_acquisition_tax(
    price: int,
    property_type: PropertyType,
    owned_house_count: int = 0,
    exclusive_area_m2: float | None = None,
) -> int:
    """취득세와 부가세(지방교육세, 농어촌특별세)의 합계."""
    raise NotImplementedError


def calc_acquisition_cost(
    listing: Listing, assumptions: ProfitAssumptions, assumed_amount: int
) -> AcquisitionCost:
    """낙찰가에 세금, 법무비, 인수금액, 명도비, 수리비, 체납 관리비를 더한 총 취득 비용."""
    raise NotImplementedError


def calc_capital_gains_tax(gain: int, holding_months: int, property_type: PropertyType) -> int:
    """양도차익과 보유 기간에 따른 양도소득세(지방소득세 포함). 차익이 없으면 0."""
    raise NotImplementedError


def simulate(
    listing: Listing,
    assumptions: ProfitAssumptions,
    assumed_amount: int,
    name: str = "기준",
) -> ProfitScenario:
    """한 가지 가정으로 실투자금, 세후 순이익, 수익률을 계산한다.

    assumptions.expected_sale_price가 반드시 채워져 있어야 한다.
    """
    raise NotImplementedError


def build_scenarios(
    listing: Listing,
    rights: RightsAnalysis,
    market: MarketComparison,
    base: ProfitAssumptions,
    target_roi: float | None = None,
) -> ProfitAnalysis:
    """보수·기준·낙관 시나리오를 만든다.

    매도가는 추정 시세를 기준으로 조정하고, 보수 시나리오는 명도 기간과 비용을 더 크게 잡는다.
    target_roi가 있으면 입찰 상한가도 계산한다.
    """
    raise NotImplementedError


def solve_max_bid(
    listing: Listing,
    base: ProfitAssumptions,
    assumed_amount: int,
    target_roi: float,
) -> int | None:
    """목표 수익률을 만족하는 가장 높은 입찰가. 최저매각가격으로도 못 맞추면 None."""
    raise NotImplementedError
