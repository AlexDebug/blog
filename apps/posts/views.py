from django.views.generic.list import ListView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth import get_user
from django.urls.base import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import HttpResponse, JsonResponse


# Create your views here.
class PostListView(ListView):
    template_name = 'posts/blog_list.html'
    model = Post


class ListDetail(SingleObjectMixin, ListView):
    model = Post
    template_name = 'posts/post.html'

    def get(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=self.model.objects.all())
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['single_object'] = self.object
        return context

    def get_queryset(self):
        return self.object.comment_set.all()


class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('posts:post')

    def form_valid(self, form):
        title = form['title'].value()
        content = form['content'].value()
        user = get_user(self.request)

        self.object = self.model(title=title, content=content, user=user)
        self.object.save()

        return redirect(self.get_success_url())


class CreteComment(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'posts/create_comment.html'
    success_url = reverse_lazy('posts:post')

    def form_valid(self, form):
        title = form['title'].value()
        content = form['content'].value()
        user = get_user(self.request)

        self.object = self.model(title=title, content=content, user=user)
        self.object.save()

        return redirect(self.get_success_url())


class DeletePost(UserPassesTestMixin, DeleteView):
    success_url = reverse_lazy('posts:post')
    model = Post

    def test_func(self):
        return self.get_object().user == get_user(self.request)


class DeleteComment(UserPassesTestMixin, DeleteView):
    success_url = reverse_lazy('posts:post')
    model = Comment

    def test_func(self):
        return self.get_object().user == get_user(self.request)


class UpdatePost(UserPassesTestMixin, UpdateView):
    form_class = PostForm
    success_url = reverse_lazy('posts:post')
    model = Post
    template_name = 'posts/update_post.html'

    def test_func(self):
        return self.get_object().user == get_user(self.request)


class UpdateComment(UserPassesTestMixin, UpdateView):
    form_class = CommentForm
    success_url = reverse_lazy('posts:post')
    model = Comment
    template_name = 'posts/update_comment.html'

    def test_func(self):
        return self.get_object().user == get_user(self.request)


@login_required()
def like(request, pk):
    post = get_object_or_404(klass=Post, pk=pk)

    if post.user == request.user:
        return HttpResponse('hola', status=404)
    elif request.user in post.dislike.all():
        return HttpResponse('hola', status=404)
    elif request.user in post.like.all():
        post.like.remove(request.user)
    else:
        post.like.add(request.user)

    return redirect(reverse_lazy('posts:post'))


@login_required
def dislike(request, pk):
    post = get_object_or_404(klass=Post,pk=pk)

    if post.user == request.user:
        return HttpResponse(status=403)
    elif request.user in post.like.all():
        return HttpResponse(status=403)
    elif request.user in post.dislike.all():
        post.dislike.remove(request.user)
    else:
        post.dislike.add(request.user)

    return redirect(reverse_lazy('posts:post'))
