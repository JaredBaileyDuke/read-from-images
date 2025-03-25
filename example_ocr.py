import pytesseract
from PIL import Image
import fitz


def convert_pdf_to_image(pdf_path):
    """
    Convert a PDF to an image file.

    Args:
        pdf_path (str): The path to the PDF file

    Returns:
        image_path (str): The path to the image file
    """
    # Open the PDF file
    pdf = fitz.open(pdf_path)
    # Get the first page
    page = pdf[0]
    # Convert the page to an image
    image = page.get_pixmap()
    # Save the image to a file
    image_path = pdf_path.replace(".pdf", ".png")
    image.save(image_path)
    # Return the path to the image file
    return image_path


def run_ocr(image_path):
    """
    Run OCR on the image at the given path and return the recognized text.

    Args:
        image_path (str): The path to the image file

    Returns:
        text (str): The recognized text
    """
    # Open the image file
    img = Image.open(image_path)
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(img)
    # Return the recognized text
    return text


if __name__ == "__main__":
    # Example image from https://www.archives.gov/files/research/jfk/releases/2025/0318/104-10012-10022.pdf
    image_path = convert_pdf_to_image('./assets/104-10012-10022.pdf')
    image = Image.open(image_path)
    text = run_ocr(image)
    print(text)
