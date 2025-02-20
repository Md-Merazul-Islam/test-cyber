from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import TeamMember
from .serializers import TeamMemberSerializer
from .permissions import IsAdminOrReadOnly
from rest_framework import pagination
class CustomPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 100
# Success response helper
def success_response(message, data=None, status_code=status.HTTP_200_OK):
    return Response({
        "success": True,
        "statusCode": status_code,
        "message": message,
        "data": data
    }, status=status_code)

# Failure response helper
def failure_response(message, error=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "success": False,
        "statusCode": status_code,
        "message": message,
        "error": error
    }, status=status_code)

# TeamMember API ViewSet


class TeamMemberViewSet(viewsets.ModelViewSet):
    queryset = TeamMember.objects.all()
    serializer_class = TeamMemberSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        team_members = self.get_queryset()
        serializer = self.get_serializer(team_members, many=True)
        return success_response("Team members retrieved successfully", serializer.data)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return failure_response("Failed to create team member", str(e))

    def update(self, request, *args, **kwargs):
        try:
            return super().update(request, *args, **kwargs)
        except Exception as e:
            return failure_response("Failed to update team member", str(e))

    def destroy(self, request, *args, **kwargs):
        try:
            return super().destroy(request, *args, **kwargs)
        except Exception as e:
            return failure_response("Failed to delete team member", str(e))
