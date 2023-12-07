from django.shortcuts import get_object_or_404

from reviews.models import Title


def title_method(request):
    title_id = request.get('title_id')
    return get_object_or_404(Title, id=title_id)
