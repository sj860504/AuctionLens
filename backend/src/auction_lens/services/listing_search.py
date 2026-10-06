from collections.abc import Sequence

from auction_lens.domain.listing import Listing, SearchCriteria
from auction_lens.ports import ListingRepository, ListingSource


class ListingSearchService:
    """경매·공매 물건 검색."""

    def __init__(self, sources: Sequence[ListingSource], repository: ListingRepository) -> None:
        self._sources = sources
        self._repository = repository

    def search(self, criteria: SearchCriteria) -> list[Listing]:
        """조건에 맞는 소스를 모두 검색해 정규화·중복 제거 후 저장하고 돌려준다."""
        raise NotImplementedError

    def get(self, listing_id: str) -> Listing:
        """저장된 물건을 조회한다. 없으면 LookupError."""
        raise NotImplementedError

    def refresh(self, listing_id: str) -> Listing:
        """소스에서 상세를 다시 받아 기일 변경·유찰·취하를 반영한다."""
        raise NotImplementedError
