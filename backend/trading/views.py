from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# add this import so you can use models.Sum(...)
from django.db import models

from .models import Inventory

@login_required
def dashboard(request):
    # increment visit counter
    visits = request.session.get('visits', 0) + 1
    request.session['visits'] = visits

    # aggregate total storage
    total_storage = (
        Inventory.objects
        .aggregate(total=models.Sum('quantity'))['total']
        or 0
    )

    return render(request, 'dashboard.html', {
        'visits': visits,
        'total_storage': total_storage,
    })
