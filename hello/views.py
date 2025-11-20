from django.shortcuts import render


def image_view(request):
    """
    Sample view that displays an image and a title.
    """
    context = {
        "title": "Hello",
        # 'image_url': 'hello/sample-image.jpg',  # Path relative to static directory
        "image_url": "https://ibb.co/Y74hq1Vj",
    }
    return render(request, 'hello/image_view.html', context)

