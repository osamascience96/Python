from datetime import datetime
from django.shortcuts import render

# Create your views here.
def index(request):
    today = datetime.now()
    return render(request, "newyear/index.html", {
        "newyear": today.day == 1 and today.month == 1
    })