from auction_lens.domain.listing import Listing
from auction_lens.domain.location import (
    Coordinate,
    StationDistance,
    TransitGrade,
    TransitProximity,
)
from auction_lens.ports import Geocoder, StationFinder, WalkingRouter

STATION_AREA_M = 500
NEAR_STATION_M = 1000
# 경로 API가 없을 때의 추정 계수
WALKING_DETOUR_FACTOR = 1.3
WALKING_M_PER_MINUTE = 80


class TransitProximityService:
    """가까운 지하철역까지의 거리 분석."""

    def __init__(
        self,
        geocoder: Geocoder,
        station_finder: StationFinder,
        router: WalkingRouter | None = None,
    ) -> None:
        self._geocoder = geocoder
        self._station_finder = station_finder
        self._router = router

    def locate(self, listing: Listing) -> Coordinate | None:
        """물건의 좌표. 이미 있으면 그대로, 없으면 주소로 변환한다."""
        raise NotImplementedError

    def nearest_stations(
        self, coordinate: Coordinate, radius_m: int = 1500, limit: int = 3
    ) -> list[StationDistance]:
        """반경 내 역을 가까운 순으로 돌려준다. 도보 거리는 경로 API, 없으면 직선거리로 추정."""
        raise NotImplementedError

    def grade(self, nearest: StationDistance | None) -> TransitGrade:
        """가장 가까운 역의 직선거리로 역세권 등급을 매긴다."""
        raise NotImplementedError

    def analyze(self, listing: Listing) -> TransitProximity:
        """좌표 변환부터 등급까지 실행한다. 좌표를 얻지 못하면 LookupError."""
        raise NotImplementedError
