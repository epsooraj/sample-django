from django.shortcuts import render


def image_view(request):
    """
    Sample view that displays an image and a title.
    """
    context = {
        "title": "Hello",
        # 'image_url': 'hello/sample-image.jpg',  # Path relative to static directory
        "image_url": "https://test-buck-ep.s3.us-east-1.amazonaws.com/sample-image.jpg?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Content-Sha256=UNSIGNED-PAYLOAD&X-Amz-Credential=ASIAZUBWOA26U2TQADTG/20251120/us-east-1/s3/aws4_request&X-Amz-Date=20251120T104619Z&X-Amz-Expires=300&X-Amz-Security-Token=IQoJb3JpZ2luX2VjECsaCXVzLWVhc3QtMSJIMEYCIQDaCJRAdpEg5nTMJcmp9dbzk6/QdWMc7ZXhAEoCnQmNUwIhANC7Nvxh4qRsGSxGnsGn5fPNkIrtYxI/w2T+5giF/6xvKuMCCPT//////////wEQABoMNjYxNTM5MTI5MDIxIgwlgTjWYjx9mf6DMesqtwIJlzEyyogxbEAAaOkPY5v/oisG6Z1NQozkAGoep7aQu5kuSNZq2DNaoSQRWPFqynzp0jlSuOGIzBrxkEia7RNO0dtKP2Ugtiexf+B4ylePyzHaoUc2M0kmmeSMaRoAfcaU/mefcskJvBFAIB1wmRJDIiRTU/Bw/xKBzvJQa1J+Mp/wuqCwORcsGNq2OBzLTJD+SsVN9R3xr4r29PHfQLFpr6M2Bc0M0sSBHMfZGpxsWEIoDofkhgSOGJV7KyO10wrUWQJD1XEM0yKU4OCAqox63YqjSduABN0MphibiZ5lPOMOvNCSmNkgy2MaESK6QRPHFXUP72SUYTUMN33HxCF/+DjJHjiONxUaIVuT0KrXRWp2ESyX/iY0nm/KxFQrcQauR04NXPOku2hrKBNj/cFTw3Y2etuaFDDQivvIBjqsAoeEjBqBNZYqFG3DmuDNoWotHxvNiB4C0SxoFI4cTPJevoRoMrWZ73kHiLbHdTLHu7QhBRWn858yUdu0PZ0vaGz2AK/QSEcC0PUjJJEXqMOZtSOhZlgzgqBF0Cp2PAlxt5yHLMjdc94zfjLNztVvGg1ejiSzpKl/Ps5dE3nqp24qCYZs/0292py5BW1tpQP8n/63kZQwZmf1OT9WYcnUHs60pzVOVoMpeYPIbXuSuv/2SKGSjNbogvJ1qvQWDrZZQcCN8xVzW7lWcjw1aGa83YcmBWxCO3aoqhOULbP0/vx16Ggh7bR/HjL/DT0ZOld5IcyfIRmilYa0fC9xgMAaYLi2beiRwp0pbJYeUvFDlDMPDcsobyjfbVMdmP6fpSLmZ6c8AMsglVN2NXMkcw%3D%3D&X-Amz-Signature=59a2930f6cdfd51b544dc979c560c47e43cb49c8a314a96f1ab0889898d148b9&X-Amz-SignedHeaders=host&response-content-disposition=inline",
    }
    return render(request, 'hello/image_view.html', context)

