from pdf2image import convert_from_path
from datetime import datetime
import pathlib
import shutil
import os

class Pdf2ImgClass:
    def __init__(self, data_path, parent_path):
        self.data_path = data_path
        self.parent_path = parent_path

    def get_poppler_path(self):
        pdftoppm_path = shutil.which("pdftoppm")
        if pdftoppm_path:
            return pathlib.Path(pdftoppm_path).parent
        else:
            return None
        
    def get_pdf_list(self):
        pdf_files = []
        try:
            pdf_files = [f for f in os.listdir(self.data_path) if f.endswith('.pdf')]
            result = []
            for pdf_file in pdf_files:
                result.append(os.path.join(self.data_path, pdf_file))
                print(os.path.join(self.data_path, pdf_file))
            return result
        except OSError as e:
            print(f"Error accessing files: {e}")
            # Handle the exception as per your requirements
            # You may choose to log the error, notify the user, or take other appropriate action
            return []

    def pdf2img(self):
        pdf_list = self.get_pdf_list()

        for index, pdf_path in enumerate(pdf_list):
            current_time = datetime.now().strftime('%y_%m_%d_%H_%M_%S')
            result_path = os.path.join(self.parent_path, "images")
            os.makedirs(result_path, exist_ok=True)  # This line will create the directory if it doesn't exist

            poppler_path = self.get_poppler_path()
            print("poppler_path", poppler_path)

            try:
                images = convert_from_path(str(pdf_path), poppler_path=poppler_path)
                for i, img in enumerate(images):
                    img.save(f'{result_path}/output_{index}_{current_time}_{i}.jpg', 'JPEG')
                
                result = "success"
                print("Result:", result)

            except Exception as e:
                result = f"An error occurred: {e}"
                print("Result:", result)