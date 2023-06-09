from rest_framework import serializers
from .models import Post, Collective, Image, Event

class CollectiveSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=100)
    
    class Meta:
        model = Collective
        fields = '__all__'
        # ['id', 'name', 'description', 'created', 'members', 'private']

class PostSerializer(serializers.ModelSerializer):

    # username = serializers.ReadOnlyField(source='get_username')

    class Meta:
        model = Post
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'

class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = '__all__'



# class CommentSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Comment
#         fields = '__all__'
