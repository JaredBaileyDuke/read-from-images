import openai
import base64
import requests

# Configure OpenAI client to use llamafile
openai.api_base = "http://localhost:8080/v1"  
openai.api_key = "sk-no-key-required"  

def call_llamafile_with_image(image_path, prompt):
    """
    Sends an image in Base64 format to llamafile and retrieves a response.

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

        # Construct the payload in OpenAI format
        payload = {
            "model": "llava",  # Change this based on available models
            "messages": [
                {"role": "system", "content": "You are an AI that can recognize text in images."},
                {"role": "user", "content": prompt, "image": base64_image}
            ]
        }

        # Send request
        headers = {"Content-Type": "application/json"}
        response = requests.post(f"{openai.api_base}/chat/completions", json=payload, headers=headers)

        # Check response
        if response.status_code != 200:
            return f"Error {response.status_code}: {response.text}"

        # Extract response text
        response_json = response.json()
        return response_json["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    image_path = "./assets/license_plate_3.png"
    prompt = "What does the license plate say?"
    
    response_text = call_llamafile_with_image(image_path, prompt)
    print("Llamafile Response:", response_text)
