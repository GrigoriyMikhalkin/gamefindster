from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User

# Create your views here.

def user_page(request,id):
    user = get_object_or_404(User,id=id)
    events = user.participation_set.all()

    context = {
        "user": user,
        "events": events,
        "request": request
    }
    return render(request, "social/userpage.html", context)
