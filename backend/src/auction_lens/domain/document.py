from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum
from typing import Any


class DocumentType(StrEnum):
    SALE_SPECIFICATION = "sale_specification"  # 매각물건명세서
    STATUS_REPORT = "status_report"  # 현황조사서
    APPRAISAL = "appraisal"  # 감정평가서
    REGISTRY = "registry"  # 등기사항전부증명서
    BUILDING_LEDGER = "building_ledger"  # 건축물대장
    PUBLIC_SALE_NOTICE = "public_sale_notice"  # 공매 공고·재산명세
    PHOTO = "photo"
    OTHER = "other"


@dataclass(frozen=True)
class DocumentRef:
    """소스에 있는, 아직 내려받지 않은 문서."""

    listing_id: str
    type: DocumentType
    title: str
    url: str


@dataclass
class Document:
    id: str
    listing_id: str
    type: DocumentType
    title: str
    file_path: str  # DATA_DIR 기준 상대 경로
    sha256: str
    acquired_at: datetime
    source_url: str = ""
    uploaded_by_user: bool = False


@dataclass
class ParsedDocument:
    document_id: str
    type: DocumentType
    text: str
    fields: dict[str, Any] = field(default_factory=dict)  # 문서 종류별 구조화 추출값
    parser_version: str = ""
    warnings: list[str] = field(default_factory=list)  # 읽지 못했거나 불확실한 항목
