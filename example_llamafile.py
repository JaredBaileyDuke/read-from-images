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
            "model": "llava",  # Ensure the model supports vision inputs
            "messages": [
                {"role": "system", "content": "You are an AI that can recognize text in images."},
                {"role": "user", "content": prompt}
            ],
            "image": base64_image  # Move image outside of messages
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

def call_llamafile_text(prompt: str, model: str = "llama", system: str | None = None,
                        temperature: float = 0.2, max_tokens: int = 512) -> str:
    """
    Sends a text prompt to llamafile and returns text back.

    Args:
        prompt: User prompt text.
        model: Model name exposed by your llamafile server (e.g., "llama").
        system: Optional system message.
        temperature: Sampling temperature.
        max_tokens: Max tokens to generate.

    Returns:
        Assistant response text (or an error string).
    """
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_tokens": max_tokens,
    }

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai.api_key}",
    }

    try:
        resp = requests.post(f"{openai.api_base}/chat/completions",
                             json=payload, headers=headers, timeout=60)

        if resp.status_code != 200:
            return f"Error {resp.status_code}: {resp.text}"

        data = resp.json()
        return data["choices"][0]["message"]["content"]

    except Exception as e:
        return f"Error: {e}"

if __name__ == "__main__":
    # image_path = "./assets/nurse_1.png"
    # prompt = "What does the image say?"
    
    # response_text = call_llamafile_with_image(image_path, prompt)
    # print("Llamafile Response:", response_text)

    out = call_llamafile_text(
        """Can you summarize this text about Lee Harvey Oswald? It is from the JFK assassination documents and has some OCR errors: 
        ee ed ‘SFeRET a1 7PAY Ee

        D20/- 30505 2

        Ved 10012 onze — qu (as RELEASE UNE Te PPOSICENT CPP HAIRY ASUSRINRTION RECORDS ADT OF (Wa

        050 - Oe

        ates
        05/2/71

        Dear Anthony,

        traveled to Nexico,
        during the period 1959-61.
        permanently to Mexico City as a con
        Served there until August 1965. He was variqusly
        described as a translator, vice-consul, and attache.
        During this tour he attempted to cultivate a U.S.
        Government employee assigned to our embassy in Mexico
        city.

        dele

        In Septenber/October 1963, Lee Harvey Oswald
        approached the Soviet Enbassy in Mexico City in an attempt
        to get a visa allowing him to return to the USSR.
        Kostikov, as a consular officer, handled this visa
        request.’ We have no information which indicates ‘any
        relationship between these individuals other than for the
        purpose of Oswald's making his visa requdst.

        Kostikov returned to Mexico City for a second tour of
        duty in July 1968. During this tour he was again assigned
        to the consular section and was a second secretary. It
        appeared that he was tasked with following the activities
        of the Central American communist parties.-and left-wing
        groups, and he met often with members of these groups,
        reportedly providing then with funds and technical
        guidance. In July/August 1969, Kostikov made an unusual
        DY trip to Moscow lasting three weeks. (His family
        remained in Mexico.) In July 1970 he made a four-day trip
        to Havani

        Kostikov's tour in Mexico ended unexpectedly in
        September 1971, Our information indicated that he was
        not due to leave for another three to four months, and at
        the time of his departure, there was some speculation that
        the suddenness of his departure was due to the fact that
        he was known to Lyalin,""",
        model="llama",
        system="You are a helpful assistant."
    )
    print(out)
