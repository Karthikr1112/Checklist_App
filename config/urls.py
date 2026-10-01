from django.conf import settings 
from django.conf.urls.static import static 
from django.contrib import admin 
from django.urls import include, path 
from django.views.generic import RedirectView

urlpatterns = [
    path("admin/", admin.site.urls),

    path("", RedirectView.as_view(
        url="/cl/dashboard/",
        permanent=False
    )),

    path("accounts/", include("apps.accounts.urls", namespace="accounts")),
    path("dashboard/", include("apps.dashboard.urls", namespace="dashboard")),
    path("stores/", include("apps.stores.urls", namespace="stores")),
    path("visits/", include("apps.visits.urls", namespace="visits")),
    path("checklists/", include("apps.checklists.urls", namespace="checklists")),
    path("actions/", include("apps.actions.urls", namespace="actions")),
    path("schedule/", include("apps.schedule.urls", namespace="schedule")),
]
