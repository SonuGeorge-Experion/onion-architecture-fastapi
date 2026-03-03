import uuid
from typing import Callable

from fastapi import Request, Response

from app.core.logging import reset_request_id, set_request_id


class RequestIdMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        async def send_wrapper(message):
            # ensure header is present on response as well
            if message.get("type") == "http.response.start":
                headers = message.setdefault("headers", [])
                # add header
                headers.append((b"x-request-id", request_id.encode("utf-8")))
            await send(message)

        # Derive or generate a request id
        headers = dict(scope.get("headers") or [])
        incoming = headers.get(b"x-request-id")
        request_id = (incoming.decode("utf-8") if incoming else str(uuid.uuid4()))

        try:
            set_request_id(request_id)
            await self.app(scope, receive, send_wrapper)
        finally:
            reset_request_id()
