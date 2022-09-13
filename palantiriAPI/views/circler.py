"""View module for handling requests about messages"""
from datetime import date, datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from palantiriAPI.models import Circler, Circle, Invitation, CircleMember
from django.contrib.auth.models import User
from django.db.models import Q

class CirclerView(ViewSet):
    """Circle_members view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single circle_member

        Returns:
            Response -- JSON serialized circle_member
        """
        try:
            circle_member = Circler.objects.get(pk=pk)
            serializer = CirclerSerializer(circle_member)
            return Response(serializer.data)
        except Circler.DoesNotExist as ex:
            return Response({'circle_member': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get circle users 

        Returns:
            Response -- JSON serialized list of circle users
        """
        
        circlers = Circler.objects.all()
        

        email = request.query_params.get('email', None)
        if email is not None:
            try:
                user = User.objects.get(email=email)
                foundCircler = Circler.objects.get(user_id=user.id)
                serializer = CirclerSerializer(foundCircler)
                return Response(serializer.data)
            except User.DoesNotExist as ex:
                return Response({'user': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = CirclerSerializer(circlers, many=True)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for a circle_member

        Returns:
            Response -- Empty body with 204 status code
        """

        circle_member = Circler.objects.get(pk=pk)
        circle_member.name = request.data["name"]

        circle_member.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)



class CirclerSerializer(serializers.ModelSerializer):
    """JSON serializer for circle_members
    """
    class Meta:
        model = Circler
        fields = ('id', 'bio', 'user')
        depth = 1