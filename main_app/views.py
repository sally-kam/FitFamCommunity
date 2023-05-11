from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import SignUpForm, PostForm, CommentForm
from .models import Profile, Comment
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
import requests
import json
# Create your views here.
# iDY/ohuCxpLGD4yb3YtGVA==1LV8KxQR4T6PSsMs
# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def food_calorie_counter(request):
    if request.method == 'POST':
        query = request.POST['query']
        api_url = 'https://api.api-ninjas.com/v1/nutrition?query='
        api_request = requests.get(api_url + query, headers={'X-Api-Key': 'iDY/ohuCxpLGD4yb3YtGVA==1LV8KxQR4T6PSsMs'})
        try:
            food = json.loads(api_request.content)
            print(api_request.content)
        except Exception as e:
            food = "Search Error!"
            print(e)
        return render(request, 'resources/food_calorie_counter.html', {'food': food})
    else:
        return render(request, 'resources/food_calorie_counter.html', {'query': 'Enter a valid query'})



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
  msg = False
    
  if request.user.is_authenticated:
        user = request.user
        
    
        if post.likes.filter(id=user.id).exists():
            msg = True

  return render(request, 'posts/index.html', {
        'posts': posts
  })


class PostList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'posts/index.html'
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
      


class SignUp(CreateView):
  form_class = SignUpForm
  success_url = reverse_lazy('posts_index')
  template_name = 'registration/signup.html'

  def form_valid(self, form):
      response = super().form_valid(form)
      print(form.cleaned_data)
      Profile.objects.create(
         user=self.object, 
         date_of_birth=form.cleaned_data['date_of_birth'], 
         bio=form.cleaned_data['bio'])
      print("self.object", self.object)
      login(self.request, self.object)
      return response

  def form_invalid(self, form):
      return self.render_to_response(self.get_context_data(form=form, error_message='Invalid sign up - try again'))



   
@login_required
def posts_detail(request, post_id):
  post = get_object_or_404(Post, id=post_id)
  form = CommentForm()
  return render(request, 'posts/detail.html', { 'post': post, 'form':form })






class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class PostUpdate(LoginRequiredMixin, UpdateView):
  model = Post
  form_class = PostForm

class PostDelete(LoginRequiredMixin, DeleteView):
  model = Post
  success_url = '/posts'

@login_required
def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    liked = False

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True

    return HttpResponseRedirect(reverse('posts_index'))

@login_required
def like_post2(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return redirect(reverse('posts_detail', kwargs={'post_id': pk}))



class CommentCreate(LoginRequiredMixin,CreateView):
   model = Comment
   form_class = CommentForm


   def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user  
        return super().form_valid(form)

   def get_success_url(self):
        return reverse_lazy('posts_index')
   
class CommentCreate2(LoginRequiredMixin,CreateView):
   model = Comment
   form_class = CommentForm


   def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        form.instance.user = self.request.user  
        return super().form_valid(form)

   def get_success_url(self):
        return reverse_lazy('posts_detail', kwargs={'post_id': self.kwargs['pk']})
   
# class CommentUpdate(LoginRequiredMixin, UpdateView):
#   model = Comment
#   form_class = CommentForm


class CommentDelete(LoginRequiredMixin, DeleteView):
  model = Comment
  success_url = reverse_lazy('posts_index')


# def unlike_post(request, pk):
#    post = get_object_or_404(Post, pk=pk)
#    post.likes.remove(request.user)
#    return redirect('post_detail', pk=pk)

