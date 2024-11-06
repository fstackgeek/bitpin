from django.views.generic import TemplateView


class SignupView(TemplateView):
    template_name = 'signup.html'


class LoginView(TemplateView):
    template_name = 'login.html'


class PostsView(TemplateView):
    template_name = 'posts.html'
