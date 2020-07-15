from rest_framework import serializers
from urlshortner.models import UrlShortnerModel
from urlshortner.constants import HOST


class UrlShortRequest(serializers.Serializer):
    url = serializers.CharField(required=True, max_length=255)  # Long Url
    expiry = serializers.DateTimeField(required=False)


class UrlLongRequest(serializers.Serializer):
    url = serializers.CharField(required=True, max_length=64)   # Short Url

    def validate_url(self, url):
        if url.startswith(HOST):
            return url
        else:
            return serializers.ValidationError("Invalid short URL")


class UrlShortResponse(serializers.ModelSerializer):
    class Meta:
        model = UrlShortnerModel
        fields = "__all__"
