from django import template
from django.conf import settings

from symposion.reviews.models import ReviewAssignment


register = template.Library()


@register.assignment_tag(takes_context=True)
def review_assignments(context):
    request = context["request"]
    assignments = ReviewAssignment.objects.filter(user=request.user)
    return assignments

import bleach

@register.filter("bleach")
def _bleach(text):
    return bleach.clean(text, tags=settings.BLEACH_ALLOWED_TAGS)
