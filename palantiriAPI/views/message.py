"""View module for handling requests about messages"""
from datetime import date, datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from palantiriAPI.models import Message, Circler, Circle
from django.db.models import Q

class MessageView(ViewSet):
    """Messages view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single message

        Returns:
            Response -- JSON serialized message
        """
        try:
            message = Message.objects.get(pk=pk)
            serializer = MessageSerializer(message)
            return Response(serializer.data)
        except Message.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get messages 

        Returns:
            Response -- JSON serialized list of messages
        """
        
        # current_user = Circler.objects.get(user=request.auth.user)
        # circle = Circle.objects.get(circler_id=current_user.id)
        # circle_messages = Message.objects.filter(Q(circle_id=circle.id) | Q(circler_id=current_user.id))
        circle_messages = Message.objects.all()
        

        message = request.query_params.get('message', None)
        if message is not None:
            circle_messages = circle_messages.filter(id=message)

        serializer = MessageSerializer(circle_messages, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized message instance
        """
        circler = Circler.objects.get(user=request.auth.user)
        circle = Circle.objects.get(id=request.data["circle"])

        message = Message.objects.create(
            content=request.data["content"],
            date_sent=date.today(),
            circle=circle,
            circler=circler
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    # def update(self, request, pk):
    #     """Handle PUT requests for a message

    #     Returns:
    #         Response -- Empty body with 204 status code
    #     """

    #     message = Message.objects.get(pk=pk)
    #     message.title = request.data["title"]
    #     message.maker = request.data["maker"]
    #     message.number_of_players = request.data["number_of_players"]
    #     message.skill_level = request.data["skill_level"]

    #     message_type = MessageType.objects.get(pk=request.data["message_type"])
    #     message.message_type = message_type
    #     message.save()

    #     return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        message = Message.objects.get(pk=pk)
        message.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


class MessageSerializer(serializers.ModelSerializer):
    """JSON serializer for messages
    """
    class Meta:
        model = Message
        fields = ('id', 'circle', 'circler', 'content', 'date_sent')
        depth = 1