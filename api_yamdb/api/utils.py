from django.shortcuts import get_object_or_404

from reviews.models import (
    Review,
    Title
)


def title_method(request):
    title_id = request.get('title_id')
    return get_object_or_404(
        Title,
        id=title_id
    )


def review_method(request):
    review_id = request.get('review_id')
    review = get_object_or_404(
        Review,
        id=review_id,
        title=title_method(
            request
        )
    )
    return review
