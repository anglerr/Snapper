import secrets
import string
import logging
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from rest_framework.response import Response
from urlshortner.models import UrlShortnerModel
from urlshortner.utils import verify_request, BadRequestException
from urlshortner.serializer import UrlShortRequest, UrlShortResponse, UrlLongRequest
from urlshortner.constants import *

logger = logging.getLogger(__name__)


def create_new_short_url():
    status = True
    while status:
        short_url = ''.join(secrets.choice(string.ascii_letters + string.digits) for i in range(SECRETS_LENGTH))
        status = UrlShortnerModel.objects.filter(short_url=short_url).exists()
    return short_url


@api_view(["POST"])
def shorten_url(request):
    """
    API to shorten any URL, expects data in the body
    """
    try:
        json = verify_request(request, UrlShortRequest, many=False)
        short_url = create_new_short_url()
        us = UrlShortnerModel()
        us.short_url = short_url
        us.actual_url = json["url"]
        if "expiry" in json.keys():
            us.expiry_date = json["expiry"]
        us.save()
        us.short_url = HOST + us.short_url
        return Response(UrlShortResponse(us).data, status=201)
    except BadRequestException as e:
        return Response(e.msg, status=e.status)
    except Exception as e:
        logger.error(str(e))
        return Response(dict({"error": "Ah Oh! This shouldn't have happened!"}), status=500)


@api_view(["POST"])
def retrieve_url(request):
    """
    Convert short URL to actual URL. Given an short url in the body of this call,
    it will revert back with the original URL
    """
    try:
        json = verify_request(request, UrlLongRequest, many=False)
        short_url = json["url"].rsplit('/', 1)[-1]
        us = UrlShortnerModel.objects.get(short_url=short_url)
        us.short_url = HOST + us.short_url
        return Response(UrlShortResponse(us).data, status=200)
    except BadRequestException as e:
        return Response(e.msg, status=e.status)
    except UrlShortnerModel.DoesNotExist:
        return Response(dict({"error": "Short url doesn't exist or have expired!"}), status=400)
    except Exception as e:
        logger.error(str(e))
        if "ValidationError" in str(e):
            return Response(dict({"error": "Invalid short URL!"}), status=400)
        return Response(dict({"error": "Ah Oh! This shouldn't have happened!"}), status=500)


@api_view(["GET", "POST", "PUT", "DELETE"])
def redirect_short_url(request, short_url):
    """
    Redirect any short URL to the actual URL
    """
    try:
        us = UrlShortnerModel.objects.get(short_url=short_url)
        return redirect(us.actual_url)
    except UrlShortnerModel.DoesNotExist:
        return Response(dict({"error": "Short url doesn't exist or have expired!"}), status=400)
    except Exception as e:
        print(str(e))
        return Response(dict({"error": "Ah oh! Something very bad has happened!"}), status=500)
