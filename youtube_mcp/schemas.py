from typing import Any, TypedDict


class ToolError(TypedDict):
    """Standard error shape for tool responses."""

    error: str


class MessageResponse(TypedDict):
    """Simple message response shape."""

    message: str


class YouTubePageInfo(TypedDict):
    """YouTube pagination metadata."""

    totalResults: int
    resultsPerPage: int


class YouTubeListResponse(TypedDict, total=False):
    """Common YouTube list response shape."""

    kind: str
    etag: str
    nextPageToken: str
    prevPageToken: str
    pageInfo: YouTubePageInfo
    items: list[dict[str, Any]]


class YouTubeResourceResponse(TypedDict, total=False):
    """Common YouTube resource response shape (non-list)."""

    kind: str
    etag: str
    id: str
    snippet: dict[str, Any]
    contentDetails: dict[str, Any]
    statistics: dict[str, Any]
    status: dict[str, Any]


class OAuthTokenData(TypedDict, total=False):
    """OAuth token payload for Google API credentials."""

    token: str
    refresh_token: str
    token_uri: str
    client_id: str
    client_secret: str
    scopes: list[str]


ListToolResponse = YouTubeListResponse | ToolError
ResourceToolResponse = YouTubeResourceResponse | ToolError
MessageToolResponse = MessageResponse | ToolError
