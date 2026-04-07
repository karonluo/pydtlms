from pydantic import BaseModel


class SelectOption(BaseModel):
    label: str
    value: str
    color_type: str | None = None
    css_class: str | None = None


class PaginationResponseBase(BaseModel):
    total: int
    page: int = 1
    page_size: int = 10