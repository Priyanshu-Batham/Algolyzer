from django.shortcuts import get_object_or_404, render

from .models import Category, Topic


def landing_page_view(request):
    # Get all categories and topics
    categories = Category.objects.filter(parent__isnull=True)
    topics = Topic.objects.all()

    # Filtering
    category_id = request.GET.get("category")
    if category_id:
        topics = topics.filter(category_id=category_id)

    # Sorting
    sort_by = request.GET.get("sort", "created_at")
    topics = topics.order_by(sort_by)

    return render(
        request,
        "study/landing_page.html",
        {
            "categories": categories,
            "topics": topics,
            "selected_category": category_id,
            "sort_by": sort_by,
        },
    )


def topic_detail_view(request, topic_id):
    topic = get_object_or_404(Topic, id=topic_id)
    return render(request, "study/topic_detail.html", {"topic": topic})
