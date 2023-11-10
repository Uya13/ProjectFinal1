from typing import Any, Dict
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.forms.models import BaseModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import HttpResponseRedirect
from .models import Post, Response
from .forms import PostForm
from .filters import ResponseFilter
from .email_methods import send_notification_about, send_notification_about_response
from .tasks import weekly_mailing


class PostsList(ListView):
    model = Post
    ordering = '-creation_datetime'
    template_name = 'posts.html'
    context_object_name = 'posts'
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        post = form.save(commit=False)

        post.user = self.request.user

        return super().form_valid(form)


class PostEdit(LoginRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    success_url = reverse_lazy('post_list')


class ResponseList(ListView):
    model = Response
    ordering = '-creation_datetime'
    template_name = 'responses.html'
    context_object_name = 'responses'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        qs = queryset.filter(post__user=self.request.user)
        self.filterset = ResponseFilter(
            self.request.GET,
            request=self.request,
            queryset=qs
        )
        return self.filterset.qs

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


def make_response(request, pk):
    post = Post.objects.filter(id=pk).get()
    user = request.user
    data = request.POST.dict()
    response_text = data.get("response_text")

    response = Response.objects.create(
        post=post, user=user, text=response_text)
    response.save()

    send_notification_about(post, user, response_text)

    return render(request, 'post_response.html', {'post_heading': post.heading, 'text': response_text})


def remove_response(request, pk):
    response = Response.objects.filter(id=pk).get()
    response.delete()
    
    return HttpResponseRedirect(reverse_lazy('response_list'))


def change_response(request, pk):
    response = Response.objects.filter(id=pk).get()

    if response.is_accepted:
        response.do_not_accept()
    else:
        response.accept()
        send_notification_about_response(post=response.post, author=response.user)

    response.save()
    
    return HttpResponseRedirect(reverse_lazy('response_list'))
