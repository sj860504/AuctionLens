"""권리분석. 네트워크·저장소 없이 입력만으로 판정하는 순수 함수."""

from collections.abc import Sequence

from auction_lens.domain.listing import Listing
from auction_lens.domain.rights import (
    DistributionEntry,
    RegistryRight,
    RightJudgement,
    RightsAnalysis,
    RightsInput,
    RiskFlag,
    Tenant,
    TenantJudgement,
)


def find_baseline_right(rights: Sequence[RegistryRight]) -> RegistryRight | None:
    """말소기준권리를 찾는다.

    (근)저당권, (가)압류, 담보가등기, 경매개시결정등기, 배당요구했거나 경매를 신청한
    전세권 중 가장 먼저 등기된 권리.
    """
    raise NotImplementedError


def judge_rights(
    rights: Sequence[RegistryRight], baseline: RegistryRight | None
) -> list[RightJudgement]:
    """권리별 인수·소멸을 판정한다. 말소기준권리보다 늦으면 소멸, 빠르면 인수."""
    raise NotImplementedError


def judge_tenants(
    tenants: Sequence[Tenant], baseline: RegistryRight | None
) -> list[TenantJudgement]:
    """임차인별 대항력과 우선변제권을 판정한다.

    대항력은 전입신고 다음 날 0시에 생긴다. 전입일이나 보증금을 알 수 없으면 None으로 둔다.
    배당액과 인수 보증금은 simulate_distribution 이후에 채운다.
    """
    raise NotImplementedError


def simulate_distribution(
    sale_price: int,
    rights: Sequence[RegistryRight],
    tenant_judgements: Sequence[TenantJudgement],
    execution_cost: int,
    legal_dong_code: str,
) -> list[DistributionEntry]:
    """예상 낙찰가를 배당 순위에 따라 나눈다.

    집행비용 → 소액임차인 최우선변제 → 우선변제권(확정일자 임차인, 담보물권)의 일자순
    → 일반채권. 소액임차인 기준은 지역과 최선순위 담보물권 설정일로 rules/에서 찾는다.
    """
    raise NotImplementedError


def detect_risk_flags(listing: Listing, rights_input: RightsInput) -> list[RiskFlag]:
    """특이사항 원문과 물건 정보에서 유치권, 법정지상권, 지분 매각 등 주의 사항을 찾는다."""
    raise NotImplementedError


def analyze(listing: Listing, rights_input: RightsInput, expected_sale_price: int) -> RightsAnalysis:
    """권리분석 전체를 실행해 인수금액 합계와 요약을 만든다."""
    raise NotImplementedError
