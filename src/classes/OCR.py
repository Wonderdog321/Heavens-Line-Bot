import cv2
import numpy as np
import easyocr

class OCR:
    def __init__(self):
        self.reader = easyocr.Reader(['en'], gpu=True)
    def pil_to_cv2(self, pil_image):
        # Convert PIL image to OpenCV format
        return cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
    
    def extract_text(self, image):
        # Implement OCR text extraction logic here
        gray = cv2.cvtColor(self.pil_to_cv2(image), cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
        text = self.reader.readtext(thresh)
        return text[0][1] if text else None
