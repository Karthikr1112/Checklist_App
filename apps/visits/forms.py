from django import forms

from apps.checklists.models import ChecklistTemplate
from apps.stores.models import Store

from .models import AuditType, Response, Visit, VisitResponse


class StartVisitForm(forms.Form):
    store = forms.ModelChoiceField(queryset=Store.objects.filter(is_active=True))
    template = forms.ModelChoiceField(queryset=ChecklistTemplate.objects.filter(is_active=True))
    visit_date = forms.DateField(widget=forms.DateInput(attrs={"type": "date"}))
    audit_type = forms.ChoiceField(choices=AuditType.choices)

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user is not None and not user.is_admin_role:
            if user.is_inventory_team:
                self.fields["store"].queryset = self.fields["store"].queryset.filter(
                    inventory_team=user
                )
                self.fields["template"].queryset = self.fields["template"].queryset.filter(
                    audience=ChecklistTemplate.Audience.INVENTORY_TEAM
                )
            else:
                self.fields["store"].queryset = self.fields["store"].queryset.filter(
                    cluster_manager=user
                )
                self.fields["template"].queryset = self.fields["template"].queryset.filter(
                    audience=ChecklistTemplate.Audience.CLUSTER_MANAGER
                )


class VisitResponseForm(forms.ModelForm):
    response = forms.ChoiceField(
        choices=[("", "—")] + list(Response.choices),
        required=False,
        widget=forms.Select(attrs={"class": "form-select form-select-sm"}),
    )

    class Meta:
        model = VisitResponse
        fields = ("response", "observation")
        widgets = {
            "observation": forms.Textarea(attrs={"rows": 2, "class": "form-control form-control-sm"}),
        }


class PhotoUploadForm(forms.Form):
    image = forms.ImageField()
    caption = forms.CharField(required=False, max_length=200)
