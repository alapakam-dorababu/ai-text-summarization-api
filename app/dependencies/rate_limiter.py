from functools import wraps
from app.core.config import redis_client  # Import Redis client

from fastapi import HTTPException, Request


def rate_limiter(limit: int, period: int, unit: str = "seconds"):
    """
    Decorator function to implement rate limiting for both authenticated and anonymous users.

    - `limit`: Maximum number of requests allowed within the specified time period.
    - `period`: The duration in which requests are counted.
    - `unit`: The time unit (seconds, minutes, hours, days).
    """

    # Define time unit conversions to seconds
    time_units = {"seconds": 1, "minutes": 60, "hours": 3600, "days": 86400}

    # Validate the unit provided
    if unit not in time_units:
        raise ValueError(
            f"Invalid time unit '{unit}'. Choose from {list(time_units.keys())}."
        )

    # Convert period into seconds
    period_seconds = period * time_units[unit]

    def decorator(func):
        """Decorator that wraps the function to enforce rate limiting."""

        @wraps(func)
        async def wrapper(request: Request, *args, **kwargs):
            # Try to get authenticated user, or use IP for anonymous users
            user = kwargs.get("user")
            if not user:
                user = (
                    request.client.host
                )  # Use client IP as the key for anonymous users

            key = f"ratelimit:{user}"  # Unique Redis key for rate limiting
            current_requests = redis_client.incr(key)  # Increment request count

            if current_requests == 1:
                # Set expiry only on the first request within the period
                redis_client.expire(key, period_seconds)

            if current_requests > limit:
                # Get the remaining TTL (time-to-live) in seconds
                remaining_time = redis_client.ttl(key)

                # If TTL is -1 (no expiry set), manually set remaining time
                if remaining_time == -1:
                    remaining_time = period_seconds

                # Raise a 429 HTTP exception with the retry time
                raise HTTPException(
                    status_code=429,
                    detail=f"Rate limit exceeded. Try again in {remaining_time} seconds.",
                )

            # Proceed with executing the original function
            return await func(request, *args, **kwargs)

        return wrapper  # Return the decorated function

    return decorator  # Return the decorator function
