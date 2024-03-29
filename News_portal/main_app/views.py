from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import CreateView
from django.core.paginator import Paginator
from .models import Post, Author, Category, PostCategory
from .filters import PostFilter
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.core.mail import send_mail, mail_managers
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
# Ниже импорт для сигналов
from django.db.models.signals import post_save, m2m_changed
from django.dispatch import receiver, Signal
# from .tasks import add_post_send_email
# import django.dispatch
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from django.http import HttpResponseNotAllowed

def methods_not_allowed(request, *args, **kwargs):
    return HttpResponseNotAllowed(["GET"], content= "This view only GET")


@require_http_methods(["GET"])
def my_view(request):
    return HttpResponse("This view only allows GET requests.")


class NewsList(ListView):
  model = Post
  template_name = 'news.html'
  context_object_name = 'news'
  queryset = Post.objects.order_by('-dateCreation')
  paginate_by = 10

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['list_in_page'] = self.paginate_by
    return context


class NewsItem(DetailView):
  model = Post
  template_name = 'news_item.html'
  context_object_name = 'news_item'


class Search(ListView):
  model = Post
  template_name = 'search.html'
  context_object_name = 'post_search'
  ordering = ['-dateCreation']
  filter_class = PostFilter
  paginate_by = 10

  def get_queryset(self):
    queryset = super().get_queryset()
    self.filter = self.filter_class(self.request.GET, queryset=queryset)
    return self.filter.qs.all()

  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['filter'] = self.filter
    context['list_in_page'] = self.paginate_by
    context['all_posts'] = Post.objects.all()
    return context


addpost = Signal()

class CreatePost(PermissionRequiredMixin, CreateView):
    permission_required = ('main_app.add_post',)
    model = Post
    template_name = 'create_post.html'
    form_class = PostForm

    def form_valid(self, form):
        post = form.save()
        id = post.id
        a = form.cleaned_data['postCategory']
        category_object_name = str(a[0])
        addpost.send(Post, instance=post, category=category_object_name)
        return redirect(f'/news/{id}')


class EditPost(PermissionRequiredMixin, LoginRequiredMixin, UpdateView):
  permission_required = ('main_app.change_post',)
  template_name = 'edit_post.html'
  form_class = PostForm

  def get_object(self, **kwargs):
    id = self.kwargs.get('pk')
    return Post.objects.get(pk=id)


class DeletePost(LoginRequiredMixin, DeleteView):
  template_name = 'delete_post.html'
  queryset = Post.objects.all()
  success_url = '/news/'


@login_required
def add_subscribe(request, pk):
    user = request.user
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    add_subscribe = Category.objects.get(name=category_object_name)
    add_subscribe.subscribers = user
    add_subscribe.save()
    Group.objects.get_or_create(name=category_object_name)
    category_group = Group.objects.get(name=category_object_name)
    if not request.user.groups.filter(name=category_object_name).exists():
        category_group.user_set.add(user)

    send_mail(
        subject=f'News Portal: {category_object_name}',
        message=f'Привет, {request.user}! Вы подписались на уведомления о выходе новых статей в категории {category_object_name}',
        from_email='newsportal272@gmail.com',
        recipient_list=[user.email, ],
    )
    return redirect(request.META.get('HTTP_REFERER'))


@login_required
def del_subscribe(request, pk):
    category_object = PostCategory.objects.get(postThrough=pk)
    category_object_name = category_object.categoryThrough
    del_subscribe = Category.objects.get(name=category_object_name)
    del_subscribe.subscribers = None
    del_subscribe.save()
    user = request.user
    category_group = Group.objects.get(name=category_object_name)
    category_group.user_set.remove(user)

    send_mail(
        subject=f'News Portal: {category_object_name}',
        message=f'Доброго дня, {request.user}! Вы отменили уведомления о выходе новых статей в категории {category_object_name}. Нам очень жаль',
        from_email='newsportal272@gmail.com',
        recipient_list=[user.email, ],
    )
    return redirect(request.META.get('HTTP_REFERER'))

def logging_page(request):
    return render(request, 'logging_page.html')


def test_error(request):
    raise Exception
    return HttpResponseRedirect(reverse('logging_page'))


class AddComments(View):
    def post(self, request, pk):
        print(request, Post)
        return redirect('/')