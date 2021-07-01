from django.shortcuts import render, get_object_or_404, redirect
from .models import Profile, Tag, Article, User
from django.db.models import Q
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.views.generic import DetailView, TemplateView
# Login / register
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
# Create your views here.


class CustomLoginView(LoginView):
    template_name = 'login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('blog:home')


class RegisterPage(FormView):
    template_name = 'register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('blog:home')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('blog:home')
        return super(RegisterPage, self).get(*args, **kwargs)


def home(request):

    # feature articles on the home page
    featured = Article.articlemanager.filter(featured=True)[0:6]

    context = {
        'articles': featured
    }

    return render(request, 'index.html', context)


def articles(request):

    # get query from request
    query = request.GET.get('query')
    # print(query)
    # Set query to '' if None
    if query == None:
        query = ''

    # articles = Article.articlemanager.all()
    # search for query in headline, sub headline, body
    articles = Article.articlemanager.filter(
        Q(headline__icontains=query) |
        Q(sub_headline__icontains=query) |
        Q(body__icontains=query)
    )

    tags = Tag.objects.all()

    context = {
        'articles': articles,
        'tags': tags,
    }

    return render(request, 'articles.html', context)


def article(request, article):

    article = get_object_or_404(Article, slug=article, status='published')

    context = {
        'article': article
    }

    return render(request, 'article.html', context)


class GuideCreate(LoginRequiredMixin, CreateView):
    model = Article
    fields = ['headline', 'sub_headline', 'image', 'body']
    template_name = 'guide_form.html'
    success_url = reverse_lazy('blog:guide-review')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(GuideCreate, self).form_valid(form)


class GuideUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Article
    fields = ['headline', 'sub_headline', 'image', 'body']
    template_name = 'guide_form.html'
    success_url = reverse_lazy('blog:articles')

    def test_func(self):
        article = self.get_object()
        if self.request.user.id == article.author.id:
            return True
        return False


class GuideDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Article
    context_object_name = 'article'
    template_name = 'guide_delete.html'
    success_url = reverse_lazy('home:articles')

    def test_func(self):
        article = self.get_object()
        if self.request.user.id == article.author.id:
            return True
        return False


class GuideReview(LoginRequiredMixin, TemplateView):
    template_name = 'review_message.html'
