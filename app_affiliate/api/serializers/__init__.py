from rest_framework import serializers

class AffiliateSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    full_name = serializers.CharField(max_length=255)
    document_type = serializers.ChoiceField(choices=['CC', 'CE', 'NIT'])
    document_number = serializers.CharField(max_length=50)
    email = serializers.EmailField()
    status = serializers.ChoiceField(choices=['ACTIVE', 'INACTIVE'], default='ACTIVE')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)

class ContributionSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    affiliate_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=12, decimal_places=2)
    contribution_date = serializers.DateField()
    payment_method = serializers.ChoiceField(choices=['CASH', 'TRANSFER', 'CARD'])
    status = serializers.ChoiceField(choices=['ACTIVE', 'INACTIVE'], default='ACTIVE')
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
