import pytesseract
import cv2
import numpy as np
from PIL import Image

# Specify the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Users\hp\Downloads.exe'

def extract_text_from_image(image_path):
    """Extracts text from image using Tesseract OCR."""
    image = Image.open(image_path)
    text = pytesseract.image_to_string(image)
    return text

def segment_image(image_path):
    """Segments visual elements in the image using OpenCV."""
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    edged = cv2.Canny(blurred, 50, 150)
    
    contours, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    segmented_elements = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        segmented_elements.append(image[y:y+h, x:x+w])
    
    return segmented_elements
def analyze_image(image_path):
    """Combines text extraction and visual element segmentation."""
    text = extract_text_from_image(image_path)
    segmented_elements = segment_image(image_path)
    
    result = {
        'text': text,
        'segmented_elements': segmented_elements
    }
    
    return result

 

def save_segmented_elements(segmented_elements):
    """Saves the segmented elements to disk."""
    for i, elem in enumerate(segmented_elements):
        cv2.imwrite(f'segmented_element_{i}.jpg', elem)
def main():
    # Get the image file path from the user
    image_path = input("Enter the path to the image file: ")
    
    # Analyze the image
    result = analyze_image(image_path)
    
    # Print extracted text
    print("Extracted Text:")
    print(result['text'])
    
    # Save segmented elements
    print(f"Number of segmented elements: {len(result['segmented_elements'])}")
    save_segmented_elements(result['segmented_elements'])
    print("Segmented elements have been saved to the current directory.")

if __name__ == "__main__":
    main()
