from django.shortcuts import render
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView
# Create your views here.
class PostList(ListView):
    model = Post
    ordering = '-pk'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PostList, self).get_context_data()
        context['categories'] = Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        return context
    #템플릿은 모델명_list.html : post_list.html
    #매개변수 모델명_list : post_list

class PostDetail(DetailView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data() #오버라이딩 후 추가요소 context 딕셔너리에 담아 템플릿에 보낼 수 있음
        context['categories']=Category.objects.all()
        context['no_category_post_count'] = Post.objects.filter(category=None).count
        return context
    #템플릿은 모델명_detail.html : post_detail.html
    #매개변수 모델명 : post

# def index(request):
#     posts = Post.objects.all().order_by('-pk') #모든 books를 가져옴, pk역순으로 나열
#     return render(request, 'blog/index.html', {'posts': posts})
#
# def single_post_page(request, pk):
#     post1 = Post.objects.get(pk=pk)
#     return render(request, 'blog/single_post_page.html', {'post': post1})

def category_page(request,slug):
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)
    else:
        category = Category.objects.get(slug=slug)
        post_list=Post.objects.filter(category=category)
    return render(request, 'blog/post_list.html', {
        'category' : category,
        'post_list' : post_list,
        'categories' : Category.objects.all(),
        'no_category_post_count' : Post.objects.filter(category=None).count
    })

def tag_page(request, slug):
    tag = Tag.objects.get(slug=slug)
    post_list = tag.post_set.all()
    return render(request, 'blog/post_list.html',{
                  'tag' : tag,
                  'post_list' : post_list,
                  'categories': Category.objects.all(),
                  'no_category_post_count': Post.objects.filter(category=None).count
    })