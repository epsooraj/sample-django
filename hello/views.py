from django.shortcuts import render


def image_view(request):
    """
    Sample view that displays an image and a title.
    """
    context = {
        "title": "Hello",
        # 'image_url': 'hello/sample-image.jpg',  # Path relative to static directory
        "image_url": "https://test-buck-ep.s3.us-east-1.amazonaws.com/sample-image.jpg",
    }
    return render(request, 'hello/image_view.html', context)

