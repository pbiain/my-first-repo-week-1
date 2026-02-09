"""LLM processor module for generating podcast scripts."""
import os
from openai import OpenAI

def generate_script(text):
    """Generate a podcast script from text using OpenAI's GPT.
    
    Args:
        text: Input text to convert to script
        
    Returns:
        Generated podcast script
    """
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    
    prompt = f"""Convert the following text into a SHORT engaging podcast script.
    Make it conversational, informative, and around 30 seconds long (approximately 75-90 words).
    Keep it brief and to the point. You can format it as simple dialogue or a host monologue.
    
    Text:
    {text}
    
    Podcast Script:"""
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a professional podcast scriptwriter. Create engaging, concise dialogue for short 30-second podcasts."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=200
    )
    
    return response.choices[0].message.content
