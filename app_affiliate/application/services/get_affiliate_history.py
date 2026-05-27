from typing import Any, List
from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface
from app_affiliate.domain.interfaces.contribution_repository_interface import ContributionRepositoryInterface
from app_affiliate.domain.exceptions import AffiliateNotFoundError

class GetAffiliateHistory:
    def __init__(
        self, 
        affiliate_repository: AffiliateRepositoryInterface,
        contribution_repository: ContributionRepositoryInterface
    ):
        self.affiliate_repository = affiliate_repository
        self.contribution_repository = contribution_repository

    def execute(self, affiliate_id: int) -> List[Any]:
        # Validate affiliate exists
        affiliate = self.affiliate_repository.get_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(f"Affiliate with ID {affiliate_id} not found.")
            
        return self.contribution_repository.get_history_by_affiliate(affiliate_id)
