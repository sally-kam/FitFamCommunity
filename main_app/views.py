from django.shortcuts import render, redirect
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, PostForm
from .models import Profile
from django.urls import reverse_lazy
# Create your views here.

# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def profile_index(request):
    profile = Profile.objects.filter(user=request.user)
    print(profile)
    return render(request, 'profile/profile.html', {
       'profile': profile
    })

@login_required
def posts_index(request):
  posts = Post.objects.all()
  return render(request, 'posts/index.html', {
        'posts': posts
  })

class SignUp(CreateView):
  form_class = SignUpForm
  success_url = reverse_lazy('posts_index')
  template_name = 'registration/signup.html'

  def form_valid(self, form):
      response = super().form_valid(form)
      print(form.cleaned_data)
      Profile.objects.create(user=self.object, date_of_birth=form.cleaned_data['date_of_birth'], bio=form.cleaned_data['bio'])
      print("self.object", self.object)
      login(self.request, self.object)
      return response

  def form_invalid(self, form):
      return self.render_to_response(self.get_context_data(form=form, error_message='Invalid sign up - try again'))

# def signup(request):
#   error_message = ''
#   if request.method == 'POST':
#     # This is how to create a 'user' form object
#     # that includes the data from the browser
#     form = SignUpForm(request.POST)
#     if form.is_valid():
#       # This will add the user to the database
#       user = form.save()
#       Profile.objects.create(user=user)
#       # This is how we log a user in via code
#       login(request, user)
#       return redirect('posts_index')
#     else:
#       error_message = 'Invalid sign up - try again'
#   # A bad POST or a GET request, so render signup.html with an empty form
#   form = SignUpForm()
#   context = {'form': form, 'error_message': error_message}
#   return render(request, 'registration/signup.html', context)

def posts_detail(request, post_id):
  post = Post.objects.get(id=post_id)
  return render(request, 'posts/detail.html', { 'post': post })






class PostCreate(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdate(UpdateView):
  model = Post
  form_class = PostForm

class PostDelete(DeleteView):
  model = Post
  success_url = '/posts'



