from rest_framework.views import APIView
from rest_framework.response import Response


class UserInfoView(APIView):
    def get(self, request, format=None):
        return Response(
            data={
                "id": getattr(request.user, "id", None),
                "username": getattr(request.user, "username", None),
                "email": getattr(request.user, "email", None)      
            },
            content_type=format
        )