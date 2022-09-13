"""View module for handling requests about messages"""
from datetime import date, datetime
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from palantiriAPI.models import Comment, Circler, Post
from django.db.models import Q

class CommentView(ViewSet):
    """Comments view"""

    def retrieve(self, request, pk):
        """Handle GET requests for single comment

        Returns:
            Response -- JSON serialized comment
        """
        try:
            comment = Comment.objects.get(pk=pk)
            serializer = CommentSerializer(comment)
            return Response(serializer.data)
        except Comment.DoesNotExist as ex:
            return Response({'comment': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """Handle GET requests to get comments 

        Returns:
            Response -- JSON serialized list of comments
        """
        
        # current_user = Commentr.objects.get(user=request.auth.user)
        # comment = Comment.objects.get(commentr_id=current_user.id)
        # comment_comments = Comment.objects.filter(Q(comment_id=comment.id) | Q(commentr_id=current_user.id))
        comments = Comment.objects.all()
        

        comment = request.query_params.get('comment', None)
        if comment is not None:
            comments = comments.filter(id=comment)

        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    def create(self, request):
        """Handle POST operations

        Returns
            Response -- JSON serialized comment instance
        """
        circler = Circler.objects.get(user=request.auth.user)
        post = Post.objects.get(pk=request.data["post"])
        comment = Comment.objects.create(
            content=request.data["content"],
            date_posted=date.today(),
            circler=circler,
            post=post
        )
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CommentSerializer(serializers.ModelSerializer):
    """JSON serializer for comments
    """
    class Meta:
        model = Comment
        fields = ('id', 'content', 'date_posted', 'circler', 'post')
        depth = 1