from apps.posts.views import ListDetail
from django.contrib.auth.models import User


# Create your views here.
class UserPost(ListDetail):
    model = User
    template_name = 'user/user_post.html'

    def get_queryset(self):
        return self.object.post_set.all()