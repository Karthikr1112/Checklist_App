from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render

from .models import ChecklistTemplate


@login_required
def template_list(request):
    templates = ChecklistTemplate.objects.prefetch_related("sections__questions")
    return render(request, "checklists/template_list.html", {"templates": templates})


@login_required
def template_detail(request, pk):
    template = get_object_or_404(
        ChecklistTemplate.objects.prefetch_related("sections__questions"), pk=pk
    )
    return render(request, "checklists/template_detail.html", {"template": template})
