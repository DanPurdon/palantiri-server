"""View module for handling requests about messages"""
from datetime import date, datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import serializers, status
from palantiriAPI.models import Message, Circler, Circle, Invitation, CircleMember, message
from django.db.models import Q

from palantiriAPI.views.message import MessageSerializer

class CircleView(ViewSet):
    """Circles view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single circle

        Returns:
            Response -- JSON serialized circle
        """
        try:
            circle = Circle.objects.get(pk=pk)
            serializer = CircleSerializer(circle)
            return Response(serializer.data)
        except Circle.DoesNotExist as ex:
            return Response({'circle': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get circles 

        Returns:
            Response -- JSON serialized list of circles
        """
        
        circles = Circle.objects.all()
        messages = Message.objects.all()
        circler = Circler.objects.get(user=request.auth.user)

        circle = request.query_params.get('circle', None)
        # Retrieves circle data with only the current user's messages
        if circle is not None:
            try: 
                selected_circle = Circle.objects.get(pk=circle)
                membership = CircleMember.objects.get(Q(circle_id = selected_circle.id) & Q(circler_id = circler.id))
                selected_circle_messages = messages.filter(Q(circler_id=circler.id) & Q(circle_id = selected_circle.id))
                serializer = CircleSerializer(selected_circle)
                message_serializer = MessageSerializer(selected_circle_messages, many=True)
                data = {"circle" : serializer.data, "myMessages": message_serializer.data}
                return Response(data)
            except CircleMember.DoesNotExist as ex:
                return Response({'forbidden': ex.args[0]}, status=status.HTTP_403_FORBIDDEN)
            
            

        user = request.query_params.get('current_user', None)
        # Retrieves current user's circle information
        if user is not None:
            circles = circles.filter(circler_id=circler.id)
        
        member = request.query_params.get('current_member', None)
        # Retrieves all circles that current user belongs to as a member
        if member is not None:
            circles = circles.filter(circle_members__circler_id=circler.id)

        serializer = CircleSerializer(circles, many=True)
        return Response(serializer.data)

    # def create(self, request):
    #     """Handle POST operations

    #     Returns
    #         Response -- JSON serialized circle instance
    #     """
    #     circler = Circler.objects.get(user=request.auth.user)
    #     circle = Circle.objects.get(id=request.data["circle_id"])

    #     circle = Circle.objects.create(
    #         content=request.data["content"],
    #         date_sent=date.today(),
    #         circle=circle,
    #         circler=circler
    #     )
    #     serializer = CircleSerializer(circle)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a circle

        Returns:
            Response -- Empty body with 204 status code
        """

        circle = Circle.objects.get(pk=pk)
        circle.name = request.data["name"]

        circle.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        circle = Circle.objects.get(pk=pk)
        circle.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


    @action(methods=['delete'], detail=True)
    def leave(self, request, pk):
        """Deletes user's membership from a circle"""
    
        circler = Circler.objects.get(user=request.auth.user)
        circle = Circle.objects.get(pk=pk)
        membership = CircleMember.objects.get(Q(circle_id = circle.id) & Q(circler_id = circler.id))
        membership.delete()
        return Response({'message': 'Membership removed'}, status=status.HTTP_204_NO_CONTENT)


class CircleSerializer(serializers.ModelSerializer):
    """JSON serializer for circles
    """
    class Meta:
        model = Circle
        fields = ('id', 'name', 'circler', 'circle_posts', 'circle_messages', 'circle_members', 'circle_invitees')
        depth = 1