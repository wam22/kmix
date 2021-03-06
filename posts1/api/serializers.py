from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField
    )


from accounts.api.serializers import UserDetailSerializer
 

from posts1.models import Post


class PostCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = [
            #'id',
            'title',
            'slug',
            'content',
            #'publish'
        ]


post_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',
        lookup_field='slug'
        )


class PostDetailSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    html = SerializerMethodField()
 
    class Meta:
        model = Post
        fields = [
            'url',
            'id',
            'user',
            'title',
            'slug',
            'content',
            'html',
            #'publish',
            'image',
            
        ]

    def get_html(self, obj):
        return obj.get_markdown()

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    



class PostListSerializer(ModelSerializer):
    url = post_detail_url
    user = UserDetailSerializer(read_only=True)
    image = SerializerMethodField()
    class Meta:
        model = Post
        fields = [
            'url',
            'user',
            'title',
            'content',
            #'publish',
            'slug',
            'image',
        ]

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image



""""

from posts.models import Post
from posts.api.serializers import PostDetailSerializer


data = {
    "title": "Yeahh buddy",
    "content": "New content",
    "publish": "2016-2-12",
    "slug": "yeah-buddy",
    
}

obj = Post.objects.get(id=2)
new_item = PostDetailSerializer(obj, data=data)
if new_item.is_valid():
    new_item.save()
else:
    print(new_item.errors)


"""