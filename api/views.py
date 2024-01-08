from rest_framework.decorators import api_view, permission_classes

from rest_framework.response import Response
from .serializers import ProjectSerializer
from projects.models import Project, Review, Tag
from rest_framework.permissions import IsAuthenticated, IsAdminUser


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": "/api/projects"},
        {"GET": "/api/projects/id"},
        {"POST": "/api/projects/id/vote"},
        {"POST": "/api/users/token"},
        {"POST": "/api/users/token/refresh"},
    ]
    return Response(routes)


@api_view(["GET"])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    # print("USER:", request.user)
    projects = Project.objects.all()
    # vai transformar o objeto em um JSON
    serializer = ProjectSerializer(projects, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    # vai transformar o objeto em um JSON
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data

    review, created = Review.objects.get_or_create(
        onwer=user,
        project=project,
    )

    review.value = data["value"]
    review.save()
    project.getVoteCount

    print("DATA", data)
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)
