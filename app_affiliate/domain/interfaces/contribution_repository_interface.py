from abc import ABC, abstractmethod
from typing import Any, Dict, List

class ContributionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, contribution_data: Dict[str, Any]) -> Any:
        """Save a new contribution."""
        pass

    @abstractmethod
    def get_history_by_affiliate(self, affiliate_id: int) -> List[Any]:
        """Fetch historical records of contributions for an affiliate, ordered descending by date."""
        pass

    @abstractmethod
    def get_summary_by_affiliate(self, affiliate_id: int) -> Dict[str, Any]:
        """Aggregate summary statistics of contributions for an affiliate."""
        pass

    @abstractmethod
    def switch_status(self, contribution_id: int, new_status: str) -> Any:
        """Switch the status of a contribution (e.g. for soft-delete)."""
        pass
