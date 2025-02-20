from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.timezone import make_aware
from django.http import JsonResponse
from .database import urls_collection, create_short_url  # Import MongoDB functions

# Home page rendering
def home(request):
    return render(request, "shortener/index.html")

# Shorten URL (Handles Form Submission)
def shorten_url(request):
    if request.method == "POST":
        long_url = request.POST.get("long_url")

        if not long_url:
            return render(request, "shortener/index.html", {"error": "Missing URL"})

        url_entry = create_short_url(long_url)  # Use MongoDB function
        expires_at = url_entry["expires_at"].strftime("%Y-%m-%d %H:%M:%S")

        return render(
            request,
            "shortener/index.html",
            {
                "short_url": f"http://127.0.0.1:8000/{url_entry['short_code']}",
                "expires_at": expires_at,
            },
        )

    return redirect("home")  # Redirect if accessed via GET

# Redirect to original URL
def redirect_url(request, short_code):
    url_entry = urls_collection.find_one({"short_code": short_code})

    if not url_entry:
        return JsonResponse({"error": "URL not found"}, status=404)

    # Ensure expires_at is timezone-aware before comparing
    expires_at = url_entry["expires_at"]
    if expires_at.tzinfo is None:
        expires_at = make_aware(expires_at)  # Convert to timezone-aware if naive

    if timezone.now() > expires_at:
        return JsonResponse({"error": "URL expired"}, status=410)

    # Increment click count
    urls_collection.update_one({"short_code": short_code}, {"$inc": {"clicks": 1}})
    
    return redirect(url_entry["long_url"])