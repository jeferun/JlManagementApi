from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
from app_affiliate.domain.exceptions import AffiliateNotFoundError, DuplicateDocumentError, InvalidContributionAmountError

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the custom exception handling.
    if isinstance(exc, AffiliateNotFoundError):
        return Response({"error": "Affiliate not found"}, status=status.HTTP_404_NOT_FOUND)
        
    if isinstance(exc, DuplicateDocumentError):
        return Response({"error": "An affiliate with this document already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    if isinstance(exc, InvalidContributionAmountError):
        return Response({"error": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    return response
