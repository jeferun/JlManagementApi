from typing import Any, Dict
from decimal import Decimal
from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface
from app_affiliate.domain.interfaces.contribution_repository_interface import ContributionRepositoryInterface
from app_affiliate.domain.exceptions import AffiliateNotFoundError, InvalidContributionAmountError

class RegisterContribution:
    def __init__(
        self, 
        affiliate_repository: AffiliateRepositoryInterface,
        contribution_repository: ContributionRepositoryInterface
    ):
        self.affiliate_repository = affiliate_repository
        self.contribution_repository = contribution_repository

    def execute(self, contribution_data: Dict[str, Any]) -> Any:
        affiliate_id = contribution_data.get('affiliate_id')
        
        # Validate affiliate exists and is active
        affiliate = self.affiliate_repository.get_by_id(affiliate_id)
        if not affiliate:
            raise AffiliateNotFoundError(f"Affiliate with ID {affiliate_id} not found.")
            
        if affiliate.status != 'ACTIVE':
            raise InvalidContributionAmountError("Cannot register contribution for an inactive affiliate.")
            
        # Validate positive amount
        amount = Decimal(str(contribution_data.get('amount', 0)))
        if amount <= 0:
            raise InvalidContributionAmountError("Contribution amount must be greater than zero.")
            
        return self.contribution_repository.save(contribution_data)
