from dataclasses import dataclass, field
from enum import StrEnum


@dataclass(frozen=True)
class Coordinate:
    lat: float
    lng: float


class TransitGrade(StrEnum):
    STATION_AREA = "station_area"  # 역세권: 500m 이내
    NEAR_STATION = "near_station"  # 준역세권: 1km 이내
    FAR = "far"  # 비역세권


@dataclass
class StationDistance:
    station_name: str
    lines: list[str]
    coordinate: Coordinate
    straight_m: int
    walking_m: int | None = None
    walking_minutes: int | None = None
    walking_is_estimated: bool = False  # 경로 API 없이 직선거리로 추정한 값


@dataclass
class TransitProximity:
    listing_id: str
    coordinate: Coordinate
    stations: list[StationDistance] = field(default_factory=list)  # 가까운 순
    grade: TransitGrade = TransitGrade.FAR

    @property
    def nearest(self) -> StationDistance | None:
        return self.stations[0] if self.stations else None
