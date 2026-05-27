from typing import Any, Dict
from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface

class CreateAffiliate:
    def __init__(self, affiliate_repository: AffiliateRepositoryInterface):
        self.affiliate_repository = affiliate_repository

    def execute(self, affiliate_data: Dict[str, Any]) -> Any:
        # Business rules and validations can be placed here if not purely DB-level.
        # Note: DuplicateDocumentError is raised by the repository itself on conflict.
        return self.affiliate_repository.create(affiliate_data)
