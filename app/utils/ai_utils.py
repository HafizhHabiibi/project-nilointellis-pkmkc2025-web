from google import genai
from zai import ZhipuAiClient
from markupsafe import Markup
import re
import markdown2


# Fungsi untuk mendapatkan respons AI dengan konfigurasi model sendiri
def get_ai_response(api_key, model_name, prompt, temperature=0.25, top_p=0.85, top_k=40):
    """
    Mengambil respons dari AI dengan konfigurasi model sendiri.
    
    Args:
        api_key (str): API key untuk autentikasi
        model_name (str): nama model yang digunakan
        prompt (str): teks prompt untuk AI
        temperature (float): Pengaturan suhu untuk variasi output (0.0 to 1.0)
        top_p (float): Pengaturan top-p untuk sampling (0.0 to 1.0)
        top_k (int): Pengaturan top-k untuk sampling (0 to N)
    
    Returns:
        str: Teks hasil respons AI yang telah dibersihkan dari format markdown.
    """
    # Initialize client
    client = genai.Client(api_key=api_key)
    
    # Configure model
    config = genai.types.GenerateContentConfig(
        temperature=temperature,
        top_p=top_p,
        top_k=top_k
    )
    
    # Generate content
    response = client.models.generate_content(
        model=model_name,
        contents=prompt,
        config=config
    )
    
    return get_text_from_response(response)

def get_ai_reply(api_key, model_name, prompt, temperature=0.7):
    """
    Fungsi untuk mendapatkan respons AI dengan konfigurasi model default.
    
    Args:
        api_key (str): API key untuk autentikasi
        model_name (str): nama model yang digunakan
        prompt (str): teks prompt untuk AI
        temperature (float): Pengaturan suhu untuk variasi output (0.0 to 1.0)
        top_p (float): Pengaturan top-p untuk sampling (0.0 to 1.0)
        top_k (int): Pengaturan top-k untuk sampling (0 to N)
    
    Returns:
        str: Teks hasil respons AI yang telah dibersihkan dari format markdown.
    """
    
    # Initialize client
    client = ZhipuAiClient(api_key=api_key)
    
    # Generate content
    response = client.chat.completions.create(
                    model=model_name,
                    messages=prompt,
                    temperature=temperature
                )
    
    message = response.choices[0].message.content

    # Get the text from the response
    return format_bot_message(message)

# Helper functions remain the same
def clean_markdown(text):
    """Bersihkan teks dari format markdown."""
    text = re.sub(r"\*\*(.*?)\*\*", r"\1", text)
    text = re.sub(r"__(.*?)__", r"\1", text)
    text = re.sub(r"\*(.*?)\*", r"\1", text)
    text = re.sub(r"_(.*?)_", r"\1", text)
    text = re.sub(r"`(.*?)`", r"\1", text)
    text = re.sub(r"^#+\s*", "", text, flags=re.MULTILINE)
    return text

# Helper functions remain the same
def format_bot_message(text):
    '''Format teks untuk pesan bot dengan markdown HTML'''
    html = markdown2.markdown(text)
    return Markup(html)

# Fungsi untuk mendapatkan teks dari respons Gemini
def get_text_from_response(response):
    """Extract all text from Gemini response and combine into a single string."""
    if hasattr(response, "text") and response.text:
        message = clean_markdown(response.text.strip())
        return format_bot_message(message)

    texts = []
    if hasattr(response, "candidates") and response.candidates:
        for part in response.candidates[0].content.parts:
            if hasattr(part, "text"):
                texts.append(part.text.strip())
    message = clean_markdown("\n".join(texts).strip()) if texts else ""
    return format_bot_message(message)