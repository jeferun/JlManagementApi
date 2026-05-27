from datetime import datetime
from app_affiliate.infrastructure.repositories.affiliate_repository import AffiliateRepository
from app_affiliate.infrastructure.repositories.contribution_repository import ContributionRepository

class GetGlobalDashboard:
    def __init__(self, affiliate_repo: AffiliateRepository, contribution_repo: ContributionRepository):
        self.affiliate_repo = affiliate_repo
        self.contribution_repo = contribution_repo

    def execute(self):
        now = datetime.now()
        active_affiliates = self.affiliate_repo.get_total_active_count()
        totals = self.contribution_repo.get_global_totals(now.month, now.year)
        
        return {
            'total_active_affiliates': active_affiliates,
            'total_monthly_contributions': totals['total_monthly'],
            'total_accumulated_contributions': totals['total_accumulated']
        }
