"""Mock progress bar interface."""

from typing import Any


class MockProgressBar:
    """A mock progressbar class that does nothing."""

    def __init__(self) -> None:
        """Initialize a mock progressbar class that does nothing."""
        ...

    def update(self, *args: Any, **kwargs: Any) -> None:
        """Do nothing."""
        ...

    def close(self) -> None:
        """Do nothing."""
        ...
