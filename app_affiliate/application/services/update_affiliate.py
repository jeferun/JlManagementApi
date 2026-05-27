from typing import Any, Dict
from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface

class UpdateAffiliate:
    def __init__(self, affiliate_repository: AffiliateRepositoryInterface):
        self.affiliate_repository = affiliate_repository

    def execute(self, affiliate_id: int, affiliate_data: Dict[str, Any]) -> Any:
        return self.affiliate_repository.update(affiliate_id, affiliate_data)
