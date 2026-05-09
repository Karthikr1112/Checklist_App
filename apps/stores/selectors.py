"""Read-only query helpers for Stores."""
from django.db.models import QuerySet

from apps.accounts.models import User

from .models import Store


def stores_visible_to(user: User) -> QuerySet[Store]:
    qs = Store.objects.select_related("cluster_manager", "store_manager")
    if user.is_admin_role:
        return qs
    if user.is_cluster_manager:
        return qs.filter(cluster_manager=user)
    if user.is_store_manager:
        return qs.filter(store_manager=user)
    return qs.none()
