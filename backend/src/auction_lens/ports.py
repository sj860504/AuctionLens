"""서비스가 의존하는 외부 연동 인터페이스. 구현체는 adapters/, storage/에 둔다."""

from typing import Protocol

from auction_lens.domain.document import Document, DocumentRef, DocumentType, ParsedDocument
from auction_lens.domain.listing import Listing, PropertyType, SaleType, SearchCriteria
from auction_lens.domain.location import Coordinate, StationDistance
from auction_lens.domain.market import AskingListing, DealKind, TradeRecord
from auction_lens.domain.report import ListingReport


class ListingSource(Protocol):
    """경매·공매 물건 소스 (법원경매, 온비드)."""

    name: str
    sale_type: SaleType

    def search(self, criteria: SearchCriteria) -> list[Listing]: ...

    def fetch_detail(self, listing: Listing) -> Listing: ...

    def list_documents(self, listing: Listing) -> list[DocumentRef]: ...

    def download(self, ref: DocumentRef) -> bytes: ...


class DocumentParser(Protocol):
    """문서 내용에서 텍스트와 구조화 필드를 추출한다."""

    def parse(self, document: Document, content: bytes) -> ParsedDocument: ...


class TradeDataSource(Protocol):
    """실거래가 소스 (국토교통부)."""

    def fetch_trades(
        self,
        sigungu_code: str,  # 법정동 코드 앞 5자리
        year_month: str,  # "YYYYMM"
        property_type: PropertyType,
        deal_kind: DealKind,
    ) -> list[TradeRecord]: ...


class AskingPriceSource(Protocol):
    """매물 호가 소스."""

    def fetch_asking_listings(
        self, legal_dong_code: str, property_type: PropertyType, deal_kind: DealKind
    ) -> list[AskingListing]: ...


class Geocoder(Protocol):
    def geocode(self, address: str) -> Coordinate | None: ...


class StationFinder(Protocol):
    """반경 내 지하철역을 직선거리 가까운 순으로 돌려준다."""

    def nearby_stations(self, origin: Coordinate, radius_m: int) -> list[StationDistance]: ...


class WalkingRouter(Protocol):
    def walking_route(self, origin: Coordinate, destination: Coordinate) -> tuple[int, int] | None:
        """(도보 거리 m, 소요 시간 분). 경로를 찾지 못하면 None."""
        ...


class ListingRepository(Protocol):
    def upsert(self, listing: Listing) -> None: ...

    def get(self, listing_id: str) -> Listing | None: ...

    def find(self, criteria: SearchCriteria) -> list[Listing]: ...


class DocumentStore(Protocol):
    """문서 파일과 메타데이터, 파싱 결과 저장."""

    def save(
        self,
        listing_id: str,
        type: DocumentType,
        title: str,
        content: bytes,
        source_url: str = "",
        uploaded_by_user: bool = False,
    ) -> Document:
        """같은 내용(sha256)이 이미 있으면 기존 문서를 돌려준다."""
        ...

    def read(self, document: Document) -> bytes: ...

    def list_for(self, listing_id: str) -> list[Document]: ...

    def save_parsed(self, parsed: ParsedDocument) -> None: ...

    def get_parsed(self, document_id: str) -> ParsedDocument | None: ...


class AnalysisRepository(Protocol):
    """분석 결과 스냅샷 저장."""

    def save_report(self, report: ListingReport) -> None: ...

    def latest_report(self, listing_id: str) -> ListingReport | None: ...
