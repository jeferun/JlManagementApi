from typing import Any, Dict, Optional
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface
from app_affiliate.domain.exceptions import AffiliateNotFoundError, DuplicateDocumentError
from app_affiliate.infrastructure.models import Affiliate

class AffiliateRepository(AffiliateRepositoryInterface):
    def create(self, affiliate_data: Dict[str, Any]) -> Any:
        try:
            affiliate = Affiliate.objects.create(**affiliate_data)
            return affiliate
        except IntegrityError:
            raise DuplicateDocumentError(f"Affiliate with document number {affiliate_data.get('document_number')} already exists.")

    def update(self, affiliate_id: int, affiliate_data: Dict[str, Any]) -> Any:
        try:
            affiliate = Affiliate.objects.get(id=affiliate_id)
            for key, value in affiliate_data.items():
                setattr(affiliate, key, value)
            affiliate.save()
            return affiliate
        except ObjectDoesNotExist:
            raise AffiliateNotFoundError(f"Affiliate with ID {affiliate_id} not found.")
        except IntegrityError:
            raise DuplicateDocumentError("Update failed due to duplicate document number.")

    def get_by_id(self, affiliate_id: int) -> Optional[Any]:
        try:
            return Affiliate.objects.get(id=affiliate_id)
        except ObjectDoesNotExist:
            raise AffiliateNotFoundError(f"Affiliate with ID {affiliate_id} not found.")

    def list_all(self, filters: Dict[str, Any] = None, page: int = 1, page_size: int = 10) -> Dict[str, Any]:
        queryset = Affiliate.objects.all()
        
        if filters:
            if 'full_name' in filters:
                queryset = queryset.filter(full_name__icontains=filters['full_name'])
            if 'status' in filters:
                queryset = queryset.filter(status=filters['status'])
        
        total_count = queryset.count()
        
        # Pagination
        start = (page - 1) * page_size
        end = start + page_size
        results = queryset[start:end]
        
        return {
            'total_count': total_count,
            'page': page,
            'page_size': page_size,
            'results': list(results)
        }

    def switch_status(self, affiliate_id: int, new_status: str) -> Any:
        try:
            affiliate = Affiliate.objects.get(id=affiliate_id)
            affiliate.status = new_status
            affiliate.save(update_fields=['status', 'updated_at'])
            return affiliate
        except ObjectDoesNotExist:
            raise AffiliateNotFoundError(f"Affiliate with ID {affiliate_id} not found.")
