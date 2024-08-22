from rest_framework.response import Response
from rest_framework import status

def healthz(request):
    return Response(data="OK", status=status.HTTP_200_OK)