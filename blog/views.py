from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView

from .forms import CommentForm
from .models import Post, Category, Tag
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin


class PostList(ListView):
    model= Post
    ordering = '-pk'

    def get_context_data(self, **kwargs):
        context=super(PostList,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count()
        return context


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','hook_text','content','head_image','file_upload','category']

    def form_valid(self,form):
        current_user=self.request.user
        if current_user.is_authenticated:
            form.instance.author=current_user
            return super(PostCreate,self).form_valid(form)
        else:
            return redirect('/blog/')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostDetail(DetailView):
    model= Post

    def get_context_data(self, **kwargs):
        context=super(PostDetail,self).get_context_data()
        context['categories']=Category.objects.all()
        context['no_category_post_count']=Post.objects.filter(category=None).count()
        context['comment_form']= CommentForm
        return context


class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category']
    template_name = 'blog/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request,*args,**kwargs)
        else:
            raise PermissionDenied

def category_page(request,slug):
    if slug =='no_category':
        category='?????????'
        post_list=Post.objects.filter(category=None)
    else:
        category=Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)
    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'categories': Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'category':category

        }


    )

def tag_page(request,slug):
    tag=Tag.objects.get(slug=slug)
    post_list=tag.post_set.all()


    return render(
        request,
        'blog/post_list.html',
        {
            'post_list':post_list,
            'categories': Category.objects.all(),
            'no_category_post_count' : Post.objects.filter(category=None).count(),
            'tag':tag

        }


    )

def new_comment(request,pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post,pk=pk)

        if request.method == 'POST':
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment=comment_form.save(commit=False)
                comment.post=post
                comment.author=request.user
                comment.save()
                return redirect(comment.get_absolute_url())

        return redirect(post.get_absolute_url())



    else:
        raise PermissionError




# def single_post_page(request,pk):
#     post = Post.objects.get(pk=pk)
#
#     return render(
#
#         request,
#         'blog/single_page.html',
#         {
#             'post':post,
#         }
#
#         )