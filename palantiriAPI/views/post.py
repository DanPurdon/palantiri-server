"""View module for handling requests about posts"""
from datetime import date
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from rest_framework import serializers, status
from palantiriAPI.models import Post, Comment, Circler, Circle, CircleMember
from rest_framework.decorators import action
from django.db.models import Q
from palantiriAPI.views.comment import CommentSerializer


class PostView(ViewSet):
    """Posts view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single post

        Returns:
            Response -- JSON serialized post
        """
        try:
            post = Post.objects.get(pk=pk)
            serializer = PostSerializer(post)
            return Response(serializer.data)
        except Post.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get all posts 

        Returns:
            Response -- JSON serialized list of posts
        """
        circler = Circler.objects.get(user=request.auth.user)
        comments = Comment.objects.all()
        # posts = Post.objects.filter(Q(circler_id=circler.id) | Q(circler_id=circler))
        posts = Post.objects.all()
        
        
        
        post = request.query_params.get('post', None)
        if post is not None:
            try:
                selected_post = Post.objects.get(pk=post)
                selected_post_comments = comments.filter(Q(circler_id=circler.id) & Q(post_id = selected_post.id))
                serializer = PostSerializer(selected_post)
                comment_serializer = CommentSerializer(selected_post_comments, many=True)
                data = {"post" : serializer.data, "myComments": comment_serializer.data}
                return Response(data)
            except Post.DoesNotExist as ex:
                return Response({'post': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized post instance
        """
        circler = Circler.objects.get(user=request.auth.user)
        circle = Circle.objects.get(circler_id=circler.id)

        post = Post.objects.create(
            content=request.data["content"],
            date_posted=date.today(),
            circler=circler,
            circle=circle
        )
        serializer = PostSerializer(post)
        return Response(serializer.data)

    def update(self, request, pk):
        """Handle PUT requests for an post

        Returns:
            Response -- Empty body with 204 status code
        """

        post = Post.objects.get(pk=pk)
        post.content = request.data["content"]
        # post.date_posted = request.data["date_posted"]

        # organizer = Gamer.objects.get(pk=request.data["organizer"])
        # post.organizer = organizer

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
        fields = ('id', 'circler', 'circle', 'content', 'date_posted', 'comments')
        depth = 1
