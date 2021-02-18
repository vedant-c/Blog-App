from django.shortcuts import render,get_object_or_404,redirect,reverse
from .models import Post,Author
from .forms import CommentForm, PostForm

from django.db.models import Count

from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.views.generic import ListView

# Create your views here.

def get_author(user):
    qs=Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def index(request):
    return render(request,'blog/index.html')

def get_category_count():
    queryset=Post.objects.values('categories__title').annotate(Count('categories__title'))
    return queryset

def blog(request):
    queryset=Post.objects.all()

    paginator=Paginator(queryset,4)
    page_request_var='page'
    page=request.GET.get(page_request_var)

    latest=Post.objects.order_by('-timestamp')[:3]

    category_count=get_category_count()

    try:
        paginated_queryset=paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset=paginator.page(1)
    except EmptyPage:
        paginated_queryset=paginator.page(paginator.num_pages)


    context={
        'post_list':paginated_queryset,
        'page_request_var':page_request_var,
        'latest':latest,
        'category_count':category_count,
        }

    return render(request,'blog/blog.html',context)


def post(request,id):
    latest=Post.objects.order_by('-timestamp')[:3]
    category_count=get_category_count()
    post=get_object_or_404(Post,id=id)

    form=CommentForm(request.POST or None)

    if request.method== "POST":
        if form.is_valid():
            form.instance.user=request.user
            form.instance.post=post
            form.save() 
            return redirect(reverse('post_detail',kwargs={'id':post.id}))

    context={
        'form':form,
        'post':post,
        'latest':latest,
        'category_count':category_count,
    }

    return render(request,'blog/post.html',context)

def post_create(request):
    form = PostForm(request.POST or None, request.FILES or None)
    author= get_author(request.user)

    if request.method=='POST':
        if form.is_valid():
            form.instance.author=author
            form.save()
            return redirect(reverse('post_detail',kwargs={'id':form.instance.id}))

    context={
        'form':form
    }

    return render(request,'post_create.html',context)

def post_update(request,id):
    pass

def post_delete(request,id):
    pass