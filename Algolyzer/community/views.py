from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect, render
from home.decorators import profile_required

from .models import Category, Comment, Post, Vote


def category_list(request):
    """Show all categories."""
    categories = Category.objects.all()
    return render(request, "community/category_list.html", {"categories": categories})


def post_list_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = (
        Post.objects.filter(category=category)
        .annotate(total_votes=Sum("votes__vote_type"))
        .order_by("-total_votes", "-created_at")
    )

    paginator = Paginator(posts, 5)  # Show 5 posts per page
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "community/post_list.html",
        {"category": category, "page_obj": page_obj},
    )


def post_detail(request, post_id):
    """Show post details along with comments and voting functionality."""
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()
    total_votes = post.votes.aggregate(Sum("vote_type"))["vote_type__sum"] or 0

    return render(
        request,
        "community/post_detail.html",
        {"post": post, "comments": comments, "total_votes": total_votes},
    )


@login_required
@profile_required
def add_comment(request, post_id):
    """Allow users to add comments to a post."""
    post = get_object_or_404(Post, id=post_id)

    if request.method == "POST":
        content = request.POST.get("content")
        if content:
            Comment.objects.create(post=post, author=request.user, content=content)

    return redirect("post_detail", post_id=post.id)


@login_required
@profile_required
def vote_post(request, post_id, vote_type):
    post = get_object_or_404(Post, id=post_id)
    vote_type = int(vote_type)

    # Ensure vote_type is either 1 (upvote) or -1 (downvote)
    if vote_type not in [1, -1]:
        return HttpResponseForbidden("Invalid vote type.")

    # Check if the user has already voted on this post
    existing_vote = Vote.objects.filter(post=post, user=request.user).first()

    if existing_vote:
        if existing_vote.vote_type == vote_type:
            # If the user clicks the same vote again, remove the vote (unvote)
            existing_vote.delete()
        else:
            # Otherwise, update the vote
            existing_vote.vote_type = vote_type
            existing_vote.save()
    else:
        # Create a new vote if none exists
        Vote.objects.create(post=post, user=request.user, vote_type=vote_type)

    return redirect("post_detail", post_id=post.id)
