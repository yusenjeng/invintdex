from control.models import Company
from rest_framework import serializers
from django.utils.timezone import now


class ToUpperCaseCharField(serializers.CharField):
    def to_representation(self, value):
        return value.upper()


class CompanySerializer(serializers.ModelSerializer):
    days_since_created = serializers.SerializerMethodField()
    ticker = ToUpperCaseCharField()

    class Meta:
        model = Company

        fields = '__all__'
        # fields = ('ticker', 'created')

    def get_days_since_created(self, obj):
        return (now() - obj.created).days

    def create(self, validated_data):
        """
        Create and return a new `Snippet` instance, given the validated data.
        """
        return Company.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Snippet` instance, given the validated data.
        """
        instance.ticker = validated_data.get('ticker', instance.ticker)
        instance.ticker_yahoo = validated_data.get('ticker_yahoo', instance.ticker_yahoo)
        instance.ticker_goog = validated_data.get('ticker_goog', instance.ticker_goog)
        instance.ticker_quandl = validated_data.get('ticker_quandl', instance.ticker_quandl)
        instance.sector = validated_data.get('sector', instance.sector)
        instance.industry = validated_data.get('industry', instance.industry)
        instance.name = validated_data.get('name', instance.name)
        instance.ipoyear = validated_data.get('ipoyear', instance.ipoyear)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.exchange = validated_data.get('exchange', instance.exchange)
        instance.comment = validated_data.get('comment', instance.comment)
        instance.caps = validated_data.get('caps', instance.caps)
        instance.yields = validated_data.get('yields', instance.yields)
        instance.is_etf = validated_data.get('is_etf', instance.is_etf)
        instance.save()
        return instance

