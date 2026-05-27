from app_affiliate.domain.interfaces.contribution_repository_interface import ContributionRepositoryInterface

class SoftDeleteContribution:
    def __init__(self, repository: ContributionRepositoryInterface):
        self.repository = repository

    def execute(self, contribution_id: int):
        return self.repository.switch_status(contribution_id, 'INACTIVE')
