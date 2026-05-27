from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class AffiliateRepositoryInterface(ABC):
    @abstractmethod
    def create(self, affiliate_data: Dict[str, Any]) -> Any:
        """Create a new affiliate."""
        pass

    @abstractmethod
    def update(self, affiliate_id: int, affiliate_data: Dict[str, Any]) -> Any:
        """Update an existing affiliate."""
        pass

    @abstractmethod
    def get_by_id(self, affiliate_id: int) -> Optional[Any]:
        """Retrieve an affiliate by their ID."""
        pass

    @abstractmethod
    def list_all(self, filters: Dict[str, Any] = None, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        """Retrieve a paginated list of affiliates."""
        pass

    @abstractmethod
    def switch_status(self, affiliate_id: int, new_status: str) -> Any:
        """Change the status (ACTIVE/INACTIVE) of an affiliate."""
        pass
