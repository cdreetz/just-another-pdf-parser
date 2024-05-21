import sys
from pdf2image import convert_from_path

def convert_pdf_to_jpg(pdf_path):
    images = convert_from_path(pdf_path)
    
    for i, image in enumerate(images):
        image.save(f'output_{i}.jpg', 'JPEG')

if __name__ == "__main__":
    pdf_path = sys.argv[1]
    convert_pdf_to_jpg(pdf_path)

