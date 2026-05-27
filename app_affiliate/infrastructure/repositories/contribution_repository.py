from typing import Any, Dict, List
from django.db.models import Sum
from django.core.exceptions import ObjectDoesNotExist

from app_affiliate.domain.interfaces.contribution_repository_interface import ContributionRepositoryInterface
from app_affiliate.domain.exceptions import ContributionNotFoundError
from app_affiliate.infrastructure.models import Contribution

class ContributionRepository(ContributionRepositoryInterface):
    def save(self, contribution_data: Dict[str, Any]) -> Any:
        return Contribution.objects.create(**contribution_data)

    def get_history_by_affiliate(self, affiliate_id: int) -> List[Any]:
        return list(
            Contribution.objects.filter(affiliate_id=affiliate_id, status='ACTIVE').order_by('-contribution_date')
        )

    def get_summary_by_affiliate(self, affiliate_id: int) -> Dict[str, Any]:
        queryset = Contribution.objects.filter(affiliate_id=affiliate_id, status='ACTIVE')
        
        total_amount = queryset.aggregate(total=Sum('amount'))['total'] or 0
        total_contributions = queryset.count()
        
        return {
            'affiliate_id': affiliate_id,
            'total_amount': float(total_amount),
            'total_contributions': total_contributions
        }

    def switch_status(self, contribution_id: int, new_status: str) -> Any:
        try:
            contribution = Contribution.objects.get(id=contribution_id)
            contribution.status = new_status
            contribution.save(update_fields=['status', 'updated_at'])
            return contribution
        except ObjectDoesNotExist:
            raise ContributionNotFoundError(f"Contribution with ID {contribution_id} not found.")

    def get_global_totals(self, current_month: int, current_year: int) -> Dict[str, Any]:
        active_contribs = Contribution.objects.filter(status='ACTIVE')
        
        accumulated = active_contribs.aggregate(total=Sum('amount'))['total'] or 0
        
        monthly_contribs = active_contribs.filter(
            contribution_date__year=current_year,
            contribution_date__month=current_month
        )
        monthly_total = monthly_contribs.aggregate(total=Sum('amount'))['total'] or 0
        
        return {
            'total_accumulated': float(accumulated),
            'total_monthly': float(monthly_total)
        }
