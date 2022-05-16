from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    # author = serializers.ReadOnlyField(read_only=True)

    class Meta:
        fields = ('id', 'text', 'author', 'image', 'pub_date')
        model = Post
