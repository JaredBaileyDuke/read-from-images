import openai
import base64

# Configure OpenAI client to use llamafile
openai.api_base = "http://localhost:8080/v1"  
openai.api_key = "sk-no-key-required"  

def call_llamafile_with_image(image_path, prompt):
    """
    Encodes an image in Base64 and sends it as a text-based request to llamafile.
    
    Args:
        image_path (str): Path to the image file.
        prompt (str): User prompt.

    Returns:
        str: Llamafile's response.
    """
    try:
        # Convert the image to Base64
        with open(image_path, "rb") as image_file:
            base64_image = base64.b64encode(image_file.read()).decode("utf-8")

        # Prepare the request
        messages = [
            {"role": "system", "content": "You are an AI that can process images."},
            {"role": "user", "content": f"{prompt}\nHere is the image:\n{base64_image}"}
        ]

        # Send text-based request
        response = openai.ChatCompletion.create(
            model="llama3",  # Make sure this matches your running model
            messages=messages
        )

        return response["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    image_path = "./assets/license_plate_3.png"
    prompt = "This image contains a car and license plate. What does the license plate say?"
    
    response_text = call_llamafile_with_image(image_path, prompt)
    print("Llamafile Response:", response_text)
