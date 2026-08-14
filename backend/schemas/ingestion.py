from pydantic import BaseModel, HttpUrl


class URLIngestionRequest(BaseModel):
    url: HttpUrl