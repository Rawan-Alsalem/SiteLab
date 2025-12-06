from django.shortcuts import render
from panel.models import Review
from django.shortcuts import render

def error_404(request, exception):
    return render(request, "errors/404.html", status=404)

def error_500(request):
    return render(request, "errors/500.html", status=500)

def error_403(request, exception):
    return render(request, "errors/403.html", status=403)

def error_400(request, exception):
    return render(request, "errors/400.html", status=400)



def home(request):
    top_reviews = Review.objects.all().order_by('-created_at')[:3]
    return render(request, 'main/index.html', {'top_reviews': top_reviews})

def our_services(request):
    top_reviews = Review.objects.all().order_by('-created_at')[:3]
    return render(request, 'main/our-services.html', {'top_reviews': top_reviews})

def all_reviews(request):
    reviews = Review.objects.all().order_by('-created_at')
    return render(request, 'main/all_reviews.html', {'reviews': reviews,})

