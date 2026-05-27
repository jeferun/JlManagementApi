from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action

from app_affiliate.api.serializers import AffiliateSerializer, ContributionSerializer
from app_affiliate.infrastructure.repositories.affiliate_repository import AffiliateRepository
from app_affiliate.infrastructure.repositories.contribution_repository import ContributionRepository

from app_affiliate.application.services.create_affiliate import CreateAffiliate
from app_affiliate.application.services.register_contribution import RegisterContribution
from app_affiliate.application.services.get_affiliate_summary import GetAffiliateSummary
from app_affiliate.application.services.get_affiliate_history import GetAffiliateHistory
from app_affiliate.application.services.soft_delete_affiliate import SoftDeleteAffiliate
from app_affiliate.application.services.update_affiliate import UpdateAffiliate
from app_affiliate.application.services.soft_delete_contribution import SoftDeleteContribution
from app_affiliate.application.services.get_global_dashboard import GetGlobalDashboard

class AffiliateViewSet(viewsets.ViewSet):
    """
    A simple ViewSet for listing or retrieving affiliates.
    """
    
    def list(self, request):
        repo = AffiliateRepository()
        
        # Extract filters and pagination from request
        filters = {}
        if 'full_name' in request.query_params:
            filters['full_name'] = request.query_params['full_name']
        if 'status' in request.query_params:
            filters['status'] = request.query_params['status']
            
        page = int(request.query_params.get('page', 1))
        page_size = int(request.query_params.get('page_size', 10))
        
        result = repo.list_all(filters=filters, page=page, page_size=page_size)
        serializer = AffiliateSerializer(result['results'], many=True)
        
        return Response({
            'total_count': result['total_count'],
            'page': result['page'],
            'page_size': result['page_size'],
            'results': serializer.data
        })

    def create(self, request):
        serializer = AffiliateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        repo = AffiliateRepository()
        use_case = CreateAffiliate(repo)
        
        affiliate = use_case.execute(serializer.validated_data)
        response_serializer = AffiliateSerializer(affiliate)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None):
        repo = AffiliateRepository()
        affiliate = repo.get_by_id(pk)
        if not affiliate:
            return Response({"error": "Affiliate not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AffiliateSerializer(affiliate)
        return Response(serializer.data)

    def update(self, request, pk=None):
        serializer = AffiliateSerializer(data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        repo = AffiliateRepository()
        use_case = UpdateAffiliate(repo)
        try:
            affiliate = use_case.execute(pk, serializer.validated_data)
            response_serializer = AffiliateSerializer(affiliate)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, pk=None):
        serializer = AffiliateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        repo = AffiliateRepository()
        use_case = UpdateAffiliate(repo)
        try:
            affiliate = use_case.execute(pk, serializer.validated_data)
            response_serializer = AffiliateSerializer(affiliate)
            return Response(response_serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None):
        repo = AffiliateRepository()
        use_case = SoftDeleteAffiliate(repo)
        try:
            use_case.execute(affiliate_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'], url_path='dashboard-summary')
    def global_dashboard(self, request):
        affiliate_repo = AffiliateRepository()
        contribution_repo = ContributionRepository()
        use_case = GetGlobalDashboard(affiliate_repo, contribution_repo)
        
        summary = use_case.execute()
        return Response(summary, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='summary')
    def retrieve_summary(self, request, pk=None):
        affiliate_repo = AffiliateRepository()
        contribution_repo = ContributionRepository()
        
        use_case = GetAffiliateSummary(affiliate_repo, contribution_repo)
        summary_dto = use_case.execute(affiliate_id=pk)
        
        return Response(summary_dto, status=status.HTTP_200_OK)
        
    @action(detail=True, methods=['get'], url_path='contributions')
    def retrieve_history(self, request, pk=None):
        affiliate_repo = AffiliateRepository()
        contribution_repo = ContributionRepository()
        
        use_case = GetAffiliateHistory(affiliate_repo, contribution_repo)
        history = use_case.execute(affiliate_id=pk)
        
        serializer = ContributionSerializer(history, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ContributionViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = ContributionSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        affiliate_repo = AffiliateRepository()
        contribution_repo = ContributionRepository()
        use_case = RegisterContribution(affiliate_repo, contribution_repo)
        
        contribution = use_case.execute(serializer.validated_data)
        response_serializer = ContributionSerializer(contribution)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        repo = ContributionRepository()
        use_case = SoftDeleteContribution(repo)
        try:
            use_case.execute(contribution_id=pk)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
