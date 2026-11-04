from typing import Any
from django.http import HttpRequest

from shopapp.models import Order


def context_all(request: HttpRequest) -> dict[str, Any]:

    context = {
        "orders": Order.objects.filter(user=request.user) if request.user.is_authenticated else [],
        "login": request.user.is_authenticated
    }

    return context
