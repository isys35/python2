from django.core.handlers.wsgi import WSGIRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def hello_api(request: WSGIRequest) -> Response:
    return Response({"helo": True})
