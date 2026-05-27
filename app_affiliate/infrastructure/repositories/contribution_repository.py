from typing import Any, Dict, List
from django.db.models import Sum

from app_affiliate.domain.interfaces.contribution_repository_interface import ContributionRepositoryInterface
from app_affiliate.infrastructure.models import Contribution

class ContributionRepository(ContributionRepositoryInterface):
    def save(self, contribution_data: Dict[str, Any]) -> Any:
        return Contribution.objects.create(**contribution_data)

    def get_history_by_affiliate(self, affiliate_id: int) -> List[Any]:
        return list(
            Contribution.objects.filter(affiliate_id=affiliate_id).order_by('-contribution_date')
        )

    def get_summary_by_affiliate(self, affiliate_id: int) -> Dict[str, Any]:
        queryset = Contribution.objects.filter(affiliate_id=affiliate_id)
        
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        total_contributions = queryset.count()
        
        return {
            'affiliate_id': affiliate_id,
            'total_amount': float(total_amount),
            'total_contributions': total_contributions
        }
