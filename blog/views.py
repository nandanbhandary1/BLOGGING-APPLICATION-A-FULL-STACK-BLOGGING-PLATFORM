from django.shortcuts import render, get_object_or_404
from .models import Post
from django.views.generic import ListView, View
from django.views import View
from .forms import CommentForm
from django.http import HttpResponseRedirect
from django.urls import reverse


class StartingPageView(ListView):
    template_name = "blog/index.html"
    model = Post
    ordering = ["-date"]  # order by date desc
    context_object_name = "posts"

    def get_queryset(self):
        queryset = super().get_queryset()  # DEFAULT QUERY SET WHICH FETCHES ALL POSTS
        data = queryset[:3]
        return data


class AllPostsView(ListView):
    template_name = "blog/all-posts.html"
    model = Post
    ordering = ["-date"]
    context_object_name = "all_posts"


class SinglePostView(View):
    def is_stored_post(self, request, post_id):
        stored_posts = request.session.get("stored_posts") # include info whether this post is saved in session or not 
        if stored_posts is not None:
            is_saved_for_later = post_id in stored_posts
        else:
            is_saved_for_later = False
        return is_saved_for_later
        
    
    def get(self, request, slug):
        post = Post.objects.get(slug=slug)
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": CommentForm(),
            "comments": post.comments.all().order_by("-id"),  # .comments is related name, to fetch all the comments related to this post
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)

    def post(self, request, slug):
        comment_form = CommentForm(request.POST)
        post = Post.objects.get(slug=slug)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)  # creates a model instance
            comment.post = post  # add extra data
            comment.save()  # save it to the database
            return HttpResponseRedirect(reverse("post-detail-page", args=[slug]))
        context = {
            "post": post,
            "post_tags": post.tags.all(),
            "comment_form": comment_form,
            "comments": post.comments.all().order_by("-id"), # id is added automatically when a comment is added
            "saved_for_later": self.is_stored_post(request, post.id)
        }
        return render(request, "blog/post-detail.html", context)
    
class ReadLaterView(View):
    def get(self, request): # getting that page and list of view
        stored_posts = request.session.get("stored_posts")
        context = {}
        if stored_posts is None or len(stored_posts) == 0:
            context["posts"] = []
            context["has_posts"] = False
        else:
            posts = Post.objects.filter(id__in=stored_posts) # this makes sure that we only fetch the post where the id's of that post are part of that stored post list
            context["posts"] = posts
            context["has_posts"] = True
            
        return render(request, "blog/stored-post.html", context)

    
    def post(self, request): # Control the session of the userand add this post to a list of posts which r saved to read_later
        stored_posts = request.session.get("stored_posts")
        if stored_posts is None:
            stored_posts = []  
        post_id = int(request.POST["post_id"])
        if post_id not in stored_posts:
            stored_posts.append(post_id)
            request.session["stored_posts"] = stored_posts # add data (stored posts) in the session 
        else: # remove id from stored post if it's part of it
            stored_posts.remove(post_id)
        request.session["stored_posts"] = stored_posts
        
        return HttpResponseRedirect("/")


""" 
Shows 3 latest posts in the starting page
"""


# def starting_page(request):
#     latest_posts = Post.objects.all().order_by("-date")[:3]
#     return render(request, "blog/index.html", {"posts": latest_posts})


"""
Gives u the details of all the posts present in the db
"""


# def posts(request):
#     all_posts = Post.objects.all().order_by("-date")
#     return render(request, "blog/all-posts.html", {"all_posts": all_posts})


""" 
Gives u the entire detail of the single post
"""


# def post_detail(request, slug):
#     # identified_post = Post.objects.get(slug=slug)
#     identified_post = get_object_or_404(Post, slug=slug)
#     return render(
#         request,
#         "blog/post-detail.html",
#         {"post": identified_post, "post_tags": identified_post.tags.all()},
#     )
