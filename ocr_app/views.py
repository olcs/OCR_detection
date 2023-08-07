from django.shortcuts import render
import os
import easyocr

reader = easyocr.Reader(['en'])

def index(request):
    return render(request, 'ocr_app/index.html')

def ocr(request):
    if request.method == 'POST' and request.FILES.get('image'):
        image = request.FILES['image']
        # Save the uploaded image to a temporary location
        with open(os.path.join('temp_images', image.name), 'wb') as f:
            for chunk in image.chunks():
                f.write(chunk)

        # Perform OCR on the image
        result = reader.readtext(os.path.join('temp_images', image.name))

        # Delete the temporary image after OCR
        os.remove(os.path.join('temp_images', image.name))

        # Extract the OCR result text
        texts = [text[1] for text in result]

        return render(request, 'ocr_app/ocr_result.html', {'texts': texts})
    return render(request, 'ocr_app/ocr_page.html')
        
