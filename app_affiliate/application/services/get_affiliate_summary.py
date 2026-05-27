from typing import Any, Dict
from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface
from app_affiliate.domain.interfaces.contribution_repository_interface import ContributionRepositoryInterface
from app_affiliate.domain.exceptions import AffiliateNotFoundError

class GetAffiliateSummary:
    def __init__(
        self, 
        affiliate_repository: AffiliateRepositoryInterface,
        contribution_repository: ContributionRepositoryInterface
    ):
        self.affiliate_repository = affiliate_repository
        self.contribution_repository = contribution_repository

    def execute(self, affiliate_id: int) -> Dict[str, Any]:
        # Validate affiliate exists
        affiliate = self.affiliate_repository.get_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(f"Affiliate with ID {affiliate_id} not found.")
            
        summary = self.contribution_repository.get_summary_by_affiliate(affiliate_id)
        history = self.contribution_repository.get_history_by_affiliate(affiliate_id)
        
        last_contribution_date = None
        if history:
            last_contribution_date = history[0].contribution_date

        return {
            "affiliate_id": affiliate_id,
            "total_contributed": summary.get("total_amount", 0.0),
            "contribution_count": summary.get("total_contributions", 0),
            "last_contribution_date": last_contribution_date
        }
