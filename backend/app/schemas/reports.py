from datetime import date, datetime
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, ConfigDict

# Standard Report Header
class ReportHeaderInfo(BaseModel):
    title: str
    subtitle: str
    organization: str = "Sri Lanka Air Force"
    school_name: str = "Trade Training School (TTS Ekala)"
    portal_name: str = "TTS Management Portal"
    section: str = "Operations & Training Wing"
    generated_at: str
    generated_by: str
    security_classification: str = "RESTRICTED / OFFICIAL USE ONLY"
    parameters: Dict[str, Any] = {}

    model_config = ConfigDict(from_attributes=True)


# Summary Metric Strip Item
class ReportSummaryStatItem(BaseModel):
    label: str
    value: Any
    category: Optional[str] = "info"  # success, warning, danger, primary, info, secondary
    percentage: Optional[float] = None
    subtext: Optional[str] = None


# Report Table Column Definition
class ReportTableColumn(BaseModel):
    field: str
    label: str
    align: str = "left"  # left, center, right
    min_width: Optional[str] = None
    is_badge: bool = False
    is_monospace: bool = False


# Unified Standard Report Response
class StandardReportResponse(BaseModel):
    report_type: str
    header: ReportHeaderInfo
    summary_stats: List[ReportSummaryStatItem] = []
    columns: List[ReportTableColumn] = []
    rows: List[Dict[str, Any]] = []
    total_records: int = 0
    empty_message: str = "No records found matching the specified parameters."

    model_config = ConfigDict(from_attributes=True)


# Dropdown Master Metadata for Filters
class FilterOptionItem(BaseModel):
    value: str
    label: str
    group: Optional[str] = None

class ReportFilterMetaResponse(BaseModel):
    trades: List[FilterOptionItem] = []
    courses: List[FilterOptionItem] = []
    batches: List[FilterOptionItem] = []
    ranks: List[FilterOptionItem] = []
    student_statuses: List[FilterOptionItem] = []
    parade_statuses: List[FilterOptionItem] = []
    billets: List[FilterOptionItem] = []
    subjects: List[FilterOptionItem] = []


# Export Request Payload
class ReportExportRequest(BaseModel):
    report_type: str
    format: str = "excel"  # excel, pdf
    title: Optional[str] = None
    header_info: Optional[Dict[str, Any]] = None
    summary_stats: Optional[Any] = None
    columns: List[Dict[str, Any]] = []
    rows: List[Dict[str, Any]] = []
