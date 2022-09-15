"""View module for handling requests about messages"""
from datetime import date, datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from palantiriAPI.models import Circler, Circle, Invitation, CircleMember
from django.db.models import Q

class CircleMemberView(ViewSet):
    """Circle_members view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single circle_member

        Returns:
            Response -- JSON serialized circle_member
        """
        try:
            circle_member = CircleMember.objects.get(pk=pk)
            serializer = CircleMemberSerializer(circle_member)
            return Response(serializer.data)
        except CircleMember.DoesNotExist as ex:
            return Response({'circle_member': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get circle_members 

        Returns:
            Response -- JSON serialized list of circle_members
        """
        
        # current_user = Circle_memberr.objects.get(user=request.auth.user)
        # circle_member = Circle_member.objects.get(circle_memberr_id=current_user.id)
        # circle_member_circle_members = Circle_member.objects.filter(Q(circle_member_id=circle_member.id) | Q(circle_memberr_id=current_user.id))
        circle_members = CircleMember.objects.all()
        

        circle_member = request.query_params.get('member', None)
        if circle_member is not None:
            circle_members = circle_members.filter(id=circle_member)

        circler = Circler.objects.get(user=request.auth.user)
        circle = Circle.objects.get(circler_id=circler.id)

        user = request.query_params.get('current_user', None)
        if user is not None:
            circle_members = circle_members.filter(circle_id=circle.id)

        serializer = CircleMemberSerializer(circle_members, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized circle_member instance
        """
        circler = Circler.objects.get(user=request.auth.user)
        invitation = Invitation.objects.get(id=request.data["invite"])
        circle = Circle.objects.get(id=invitation.circle_id)

        circle_member = CircleMember.objects.create(
            date_joined=date.today(),
            circle=circle,
            circler=circler
        )
        invitation.delete()
        serializer = CircleMemberSerializer(circle_member)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a circle_member

        Returns:
            Response -- Empty body with 204 status code
        """

        circler = Circler.objects.get(pk=pk)
        circler.user.username = request.data["username"]
        circler.user.first_name = request.data["first_name"]
        circler.user.last_name = request.data["last_name"]
        circler.user.email = request.data["email"]

        circler.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        circle_member = CircleMember.objects.get(pk=pk)
        circle_member.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class CircleMemberSerializer(serializers.ModelSerializer):
    """JSON serializer for circle_members
    """
    class Meta:
        model = CircleMember
        fields = ('id', 'date_joined', 'circle', 'circler')
        depth = 2