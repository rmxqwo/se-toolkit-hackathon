import time
from collections import defaultdict
from fastapi import Request, HTTPException
from app.config import settings

# In-memory rate limiter (for production, use Redis)
_request_counts: dict[str, list[float]] = defaultdict(list)


class RateLimiter:
    """Simple sliding window rate limiter."""

    def __init__(self, max_requests: int = settings.RATE_LIMIT_PER_MINUTE):
        self.max_requests = max_requests
        self.window_seconds = 60

    async def __call__(self, request: Request) -> None:
        client_ip = request.client.host
        current_time = time.time()

        # Clean old entries
        _request_counts[client_ip] = [
            t for t in _request_counts[client_ip]
            if current_time - t < self.window_seconds
        ]

        # Check limit
        if len(_request_counts[client_ip]) >= self.max_requests:
            raise HTTPException(
                status_code=429,
                detail="Too many requests. Please try again later.",
            )

        _request_counts[client_ip].append(current_time)


# Create middleware instance
rate_limiter = RateLimiter()
