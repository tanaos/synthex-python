from typing import Any, Callable, TypeVar
from functools import wraps
from pydantic import ValidationError
import inspect

from .exceptions import ValidationError as SynthexValidationError


T = TypeVar("T", bound=type)


def handle_validation_errors(cls: T) -> T:
    for attr_name in dir(cls):
        if attr_name.startswith("_"):
            # Skip private and dunder methods
            continue

        attr = getattr(cls, attr_name)
        if not callable(attr):
            continue

        # Async functions
        if inspect.iscoroutinefunction(attr):
            @wraps(attr)
            async def async_wrapper(
                self: Any, *args: Any, __attr: Callable[..., Any] = attr, **kwargs: Any
            ) -> Any:
                try:
                    return await __attr(self, *args, **kwargs)
                except ValidationError as e:
                    raise SynthexValidationError(f"Invalid input: {e}") from e
            setattr(cls, attr_name, async_wrapper)
        # Sync functions
        else:
            @wraps(attr)
            def sync_wrapper(
                self: Any, *args: Any, __attr: Callable[..., Any] = attr, **kwargs: Any
            ) -> Any:
                try:
                    return __attr(self, *args, **kwargs)
                except ValidationError as e:
                    raise SynthexValidationError(f"Invalid input: {e}") from e
            setattr(cls, attr_name, sync_wrapper)

    return cls
