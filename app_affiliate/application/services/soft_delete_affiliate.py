from app_affiliate.domain.interfaces.affiliate_repository_interface import AffiliateRepositoryInterface

class SoftDeleteAffiliate:
    def __init__(self, repository: AffiliateRepositoryInterface):
        self.repository = repository

    def execute(self, affiliate_id: int):
        return self.repository.switch_status(affiliate_id, 'INACTIVE')
