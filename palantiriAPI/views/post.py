"""View module for handling requests about posts"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import serializers, status
from palantiriAPI.models import Post, Comment, Circler
from rest_framework.decorators import action

class PostView(ViewSet):
    """Posts view"""

    # @action(methods=['post'], detail=True)
    # def signup(self, request, pk):
    #     """Post request for a user to sign up for an event"""
    
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     event = Event.objects.get(pk=pk)
    #     event.attendees.add(gamer)
    #     return Response({'message': 'Gamer added'}, status=status.HTTP_201_CREATED)

    # @action(methods=['post'], detail=True)
    # def leave(self, request, pk):
    #     """Delete request for a user to leave an event"""
    
    #     gamer = Gamer.objects.get(user=request.auth.user)
    #     event = Event.objects.get(pk=pk)
    #     event.attendees.remove(gamer)
    #     return Response({'message': 'Gamer removed'}, status=status.HTTP_204_NO_CONTENT)
    


    # def retrieve(self, request, pk):
    #     """Handle GET requests for single post

    #     Returns:
    #         Response -- JSON serialized post
    #     """
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         serializer = PostSerializer(post)
    #         return Response(serializer.data)
    #     except Post.DoesNotExist as ex:
    #         return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all posts

        Returns:
            Response -- JSON serialized list of posts
        """
        circler = Circler.objects.get(user=request.auth.user)
        user_posts = Post.objects.filter(circler_id=circler.user_id)
        
        post = request.query_params.get('post', None)
        if post is not None:
            user_posts = user_posts.filter(post_id=post)
                    
        serializer = PostSerializer(user_posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized game instance
        """
        organizer = Gamer.objects.get(user=request.auth.user)
        game = Game.objects.get(pk=request.data["game"])

        post = Post.objects.create(
            description=request.data["description"],
            date=request.data["date"],
            time=request.data["time"],
            game=game,
            organizer=organizer
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        post.description = request.data["description"]
        post.date = request.data["date"]
        post.time = request.data["time"]

        game = Game.objects.get(pk=request.data["game"])
        post.game = game

        organizer = Gamer.objects.get(pk=request.data["organizer"])
        post.organizer = organizer

        post.save()

        return Response(None, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        post = Post.objects.get(pk=pk)
        post.delete()
        return Response(None, status=status.HTTP_204_NO_CONTENT)


# class CommentSerializer(serializers.ModelSerializer):
#     """JSON serializer for posts
#     """
#     class Meta:
#         model = Comment
#         fields = ('id', 'post', 'circler', 'content', 'date_posted')

class PostSerializer(serializers.ModelSerializer):
    """JSON serializer for posts
    """
    # comments = CommentSerializer(many=True)
    class Meta:
        model = Post
        fields = ('id', 'circler', 'content', 'date_posted', 'comments')
        depth = 1
