"""View module for handling requests about messages"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from palantiriAPI.models import Message, Circler, Circle


class MessageView(ViewSet):
    """Level up messages view"""

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
        """Handle GET requests to get all messages

        Returns:
            Response -- JSON serialized list of messages
        """
        circle = Circle.objects.get(circler=request.auth.user)
        circle_messages = Message.objects.filter(circle_id=circle.circler_id)
        # message_type = request.query_params.get('type', None)
        # if message_type is not None:
        #     messages = messages.filter(message_type_id=message_type)
        serializer = MessageSerializer(circle_messages, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized message instance
        """
        messager = Messager.objects.get(user=request.auth.user)
        message_type = MessageType.objects.get(pk=request.data["message_type"])

        message = Message.objects.create(
            title=request.data["title"],
            maker=request.data["maker"],
            number_of_players=request.data["number_of_players"],
            skill_level=request.data["skill_level"],
            messager=messager,
            message_type=message_type
        )
        serializer = MessageSerializer(message)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk):
        """Handle PUT requests for a message

        Returns:
            Response -- Empty body with 204 status code
        """

        message = Message.objects.get(pk=pk)
        message.title = request.data["title"]
        message.maker = request.data["maker"]
        message.number_of_players = request.data["number_of_players"]
        message.skill_level = request.data["skill_level"]

        message_type = MessageType.objects.get(pk=request.data["message_type"])
        message.message_type = message_type
        message.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

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