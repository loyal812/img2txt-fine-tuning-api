import os
import shutil
import fitz  # PyMuPDF
import secrets

def generate_api_key():
    api_key = secrets.token_urlsafe(32)  # Generate a 32-byte (256-bit) random URL-safe API key
    return api_key

def is_image_file(file_path):
    image_extensions = {'.jpg', '.jpeg', '.png'}
    return os.path.splitext(file_path)[1].lower() in image_extensions

def is_pdf_file(file_path):
    return os.path.splitext(file_path)[1].lower() == '.pdf'

def is_text_file(file_path):
    text_extensions = {'.txt'}  # Add more text file extensions as needed
    return os.path.splitext(file_path)[1].lower() in text_extensions

def copy_file_to_folder(source_file, target_folder):
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)
    shutil.copy(source_file, target_folder)

def get_image_pages_percentage(pdf_path):
    pdf_document = fitz.open(pdf_path)
    total_pages = pdf_document.page_count
    image_pages = 0

    for page in pdf_document:
        image_objects = page.get_images()
        if image_objects:
            image_pages += 1

    pdf_document.close()

    if total_pages == 0:
        return 0.0

    percentage = (image_pages / total_pages) * 100
    print(f'image {percentage} %')
    return percentage

def has_text(pdf_path):
    pdf_document = fitz.open(pdf_path)
    for page in pdf_document:
        text = page.get_text()
        if text.strip():  # If text exists, it's not just images
            pdf_document.close()
            return True
    pdf_document.close()
    return False

def check_pdf_content(pdf_path):
    doc = fitz.open(pdf_path)

    image_count = 0
    text_count = 0

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text = page.get_text("text")

        if text:
            text_count += 1
        else:
            image_count += 1

    doc.close()

    print("image count: ", image_count)
    print("text count: ", text_count)

    if image_count > text_count:
        return "image"
    elif text_count > image_count:
        return "text"
    else:
        return "The PDF contains a combination of images and text."