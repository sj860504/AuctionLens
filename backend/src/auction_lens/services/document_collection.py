from collections.abc import Mapping

from auction_lens.domain.document import Document, DocumentType, ParsedDocument
from auction_lens.domain.listing import Listing
from auction_lens.domain.rights import RightsInput
from auction_lens.ports import DocumentParser, DocumentStore, ListingSource


class DocumentCollectionService:
    """물건 관련 문서의 수집, 파싱, 권리분석 입력 생성."""

    def __init__(
        self,
        sources: Mapping[str, ListingSource],  # Listing.source 이름으로 조회
        store: DocumentStore,
        parser: DocumentParser,
    ) -> None:
        self._sources = sources
        self._store = store
        self._parser = parser

    def collect(self, listing: Listing) -> list[Document]:
        """소스의 문서 목록을 내려받아 저장한다. 이미 받은 문서는 다시 받지 않는다."""
        raise NotImplementedError

    def register_upload(
        self, listing_id: str, doc_type: DocumentType, filename: str, content: bytes
    ) -> Document:
        """사용자가 올린 문서(등기사항증명서 등)를 등록한다."""
        raise NotImplementedError

    def parse(self, document: Document) -> ParsedDocument:
        """문서를 파싱해 결과를 저장한다. 같은 파서 버전의 결과가 있으면 재사용한다."""
        raise NotImplementedError

    def build_rights_input(self, listing_id: str) -> RightsInput:
        """파싱 결과를 합쳐 권리분석 입력을 만든다.

        등기사항증명서가 있으면 등기 권리의 기준으로 삼고, 없으면 매각물건명세서만 사용한다.
        """
        raise NotImplementedError
