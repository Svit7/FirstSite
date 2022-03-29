from django.core.mail import send_mail
from django.http import HttpResponseNotFound, HttpResponse, Http404
from django.shortcuts import redirect, render
from django.views.generic import ListView, DetailView, CreateView
from django.views.generic.edit import FormMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout, login

from .models import Women, Category, Comments, Contact
from .forms import (
    AddPostForm,
    RegisterUserForm,
    LoginUserForm,
    ContactForm,
    CommentForm,
)
from .utils import DataMixin, ValidFormMixin, CustomSuccessMessageMixin


class WomenHome(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Home page")
        return {**context, **c_def}

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('cat', 'author')


class WomenCategory(DataMixin, ListView):
    model = Women
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = True

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c = Category.objects.get(slug=self.kwargs['cat_slug'])
        c_def = self.get_user_context(title="Category - " + str(c.name),
                                      cat_selected=c.pk)
        return {**context, **c_def}

    def get_queryset(self):
        return Women.objects.filter(cat__slug=self.kwargs['cat_slug'],
                                    is_published=True).select_related('cat', 'author')


class ShowPost(DataMixin, CustomSuccessMessageMixin,
               ValidFormMixin, FormMixin, DetailView):
    model = Women
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'
    form_class = CommentForm
    success_msg = "Comment successfully created, please wait for moderation."

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title=context['post'])
        return {**context, **c_def}

    def get_success_url(self, **kwargs):
        return reverse_lazy('post', kwargs={'post_slug': self.get_object().slug})

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.post = self.get_object()
        self.object.save()
        return super().form_valid(form)

    def get_queryset(self):
        return Women.objects.filter(is_published=True).select_related('author')


class AddPage(DataMixin, ValidFormMixin, CreateView):
    model = Women
    form_class = AddPostForm
    template_name = 'women/addpage.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Add post")
        return {**context, **c_def}


class ContactFormView(DataMixin, ValidFormMixin, CreateView):
    model = Contact
    form_class = ContactForm
    template_name = 'women/contact.html'
    success_url = reverse_lazy('home')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Contact")
        return {**context, **c_def}

    def form_valid(self, form):
        # Forming a message to send
        data = form.data
        subject = f'Message from user: "{data["name"]}" Sender email: "{data["email"]}"'
        email(subject, data['content'])
        return super().form_valid(form)


def email(subject, content):
    send_mail(subject, content,
              'from@example.com',
              ['to@example.com'],
              fail_silently=False,
              )


class AboutSite(DataMixin, ListView):
    model = Women
    template_name = 'women/about.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="About us")
        return {**context, **c_def}


class RegisterUser(DataMixin, CreateView):
    form_class = RegisterUserForm
    template_name = 'women/register.html'
    success_url = reverse_lazy('login')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sing up")
        return {**context, **c_def}

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('home')


class LoginUser(DataMixin, LoginView):
    form_class = LoginUserForm
    template_name = 'women/login.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        c_def = self.get_user_context(title="Sing in")
        return {**context, **c_def}

    def get_success_url(self):
        return reverse_lazy('home')


def logout_user(request):
    logout(request)
    return redirect('login')


def comment_status(request, pk, type):
    # post = get_object_or_404(Women, slug=post, status='published')
    #
    # allcomments = post.comments.filter(status=True)
    # page = request.GET.get('page', 1)
    #
    # paginator = Paginator(allcomments, 10)
    #
    # try:
    #     comments = paginator.page(page)
    # except PageNotAnInteger:
    #     comments = paginator.page(1)
    # except EmptyPage:
    #     comments = paginator.page(paginator.num_pages)

    try:
        item = Comments.objects.get(pk=pk)

        if request.user != item.post.author:
            return HttpResponse('Error post author')
        if type == 'public':
            import operator
            item.status = operator.not_(item.status)
            item.save()
            template = 'women/comment_item.html'
            context = {'node': item, 'status_accept': 'Comment accept', 'status_decline': 'Comment decline'}
            return render(request, template, context)
        elif type == 'delete':
            item.delete()
            return HttpResponse('''
			<h5>Comment delete</h5>
			''')
        return HttpResponse('!')
    except Comments.DoesNotExist(pk=pk):
        raise Http404('<h1>Page not found. Error 404.</h1>')


def pageNotFound(request, exception):
    return HttpResponseNotFound('<h1>Page not found. Error 404.</h1>')
