"""View module for handling requests about messages"""
from datetime import date, datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from palantiriAPI.models import Circler, Circle, Invitation
from django.db.models import Q

class InvitationView(ViewSet):
    """Invitations view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single invitation

        Returns:
            Response -- JSON serialized invitation
        """
        try:
            invitation = Invitation.objects.get(pk=pk)
            serializer = InvitationSerializer(invitation)
            return Response(serializer.data)
        except Invitation.DoesNotExist as ex:
            return Response({'invitation': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get invitations 

        Returns:
            Response -- JSON serialized list of invitations
        """
        
        invitations = Invitation.objects.all()
        circler = Circler.objects.get(user=request.auth.user)

        invitation = request.query_params.get('invitation', None)
        if invitation is not None:
            invitations = invitations.filter(id=invitation)
        
        circle = Circle.objects.get(circler_id=circler.id)

        user = request.query_params.get('current_user', None)
        # Retrieves all invitations TO the current user's circle
        if user is not None:
            invitations = invitations.filter(circle_id=circle.id)
        
        member = request.query_params.get('current_member', None)
        # Retrieves all invitations to other circles for the current user
        if member is not None:
            invitations = invitations.filter(circler_id=circler.id)

        serializer = InvitationSerializer(invitations, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized invitation instance
        """
        invitee = Circler.objects.get(pk=request.data["invitee"])
        sender = Circler.objects.get(user=request.auth.user)
        circle = Circle.objects.get(circler_id=sender.id)

        invitation = Invitation.objects.create(
            circle=circle,
            circler=invitee
        )
        serializer = InvitationSerializer(invitation)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a invitation

        Returns:
            Response -- Empty body with 204 status code
        """

        invitation = Invitation.objects.get(pk=pk)
        invitation.name = request.data["name"]

        invitation.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        invitation = Invitation.objects.get(pk=pk)
        invitation.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class InvitationSerializer(serializers.ModelSerializer):
    """JSON serializer for invitations
    """
    class Meta:
        model = Invitation
        fields = ('id', 'circle', 'circler')
        depth = 2