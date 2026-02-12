import os
import re
import gradio as gr
from dotenv import load_dotenv
import importlib
from pathlib import Path  # Fixed the NameError

# --- 1. ENVIRONMENT SETUP ---
# .parent is 'Day 1'
# .parent.parent is 'WEEK 2'
# .parent.parent.parent is 'IRONHACK-BOOTCAMP' (where your .env is)
load_dotenv("/.env")

# Verify API Key
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌ ERROR: OPENAI_API_KEY not found. Check your .env file.")
else:
    print("✅ API Key loaded successfully!")

# --- 2. IMPORT CUSTOM MODULES ---
import src.data_processor as dp
import src.llm_processor as lp
import src.tts_generator as tg

# --- 3. HELPER FUNCTIONS ---
def chunk_text_by_sentences(text, max_chars=4000):
    """Splits text into chunks without breaking sentences."""
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)
    chunks = []
    current_chunk = ""
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 <= max_chars:
            current_chunk += (sentence + " ")
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "
    if current_chunk:
        chunks.append(current_chunk.strip())
    return chunks

def create_podcast(input_text, speaker_voice, file_input):
    """Main logic wrapper for the Gradio Interface."""
    print(f"🎙️ Process started for voice: {speaker_voice}")
    try:
        # Step A: Process Input (URL, Text, or PDF)
        content = dp.process_input(input_text, file_input)
        if not content or content.strip() == "":
            return "⚠️ Error: No content found to process.", None

        # Step B: Generate Script via LLM (chunked for long inputs)
        chunks = chunk_text_by_sentences(content, max_chars=2000)
        scripts = []
        for idx, chunk in enumerate(chunks, start=1):
            print(f"--- Generating Script Chunk {idx}/{len(chunks)} ---")
            scripts.append(lp.generate_script(chunk))
        script = "\n\n".join(scripts).strip()

        # Step C: Generate Audio via TTS
        print("--- Generating Audio ---")
        audio_path = tg.generate_audio(script, voice=speaker_voice)

        return script, audio_path
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return f"An error occurred: {str(e)}", None

# --- 4. GRADIO UI LAYOUT ---
with gr.Blocks(title="AI Podcast Studio") as demo:
    gr.Markdown("# 🎙️ AI Podcast Studio")
    gr.Markdown("Convert your notes, PDFs, or URLs into a spoken podcast script.")
    
    with gr.Row():
        with gr.Column():
            input_data = gr.Textbox(label="URL or Text Input", placeholder="Paste text or a link here...")
            file_input = gr.File(label="Upload PDF", file_types=[".pdf"])
            voice_opt = gr.Dropdown(
                choices=["Alloy", "Echo", "Fable", "Onyx", "Nova", "Shimmer"], 
                label="Select Voice", 
                value="Alloy"
            )
            generate_btn = gr.Button("🚀 Generate Podcast", variant="primary")
            
        with gr.Column():
            script_out = gr.Textbox(label="Generated Script", interactive=False)
            audio_out = gr.Audio(label="Resulting Podcast Audio")

    # Define the Button Action
    generate_btn.click(
        fn=create_podcast,
        inputs=[input_data, voice_opt, file_input],
        outputs=[script_out, audio_out]
    )

# --- 5. PROTECTED EXECUTION ---
if __name__ == "__main__":
    # Close any existing Gradio instances to prevent port conflicts
    gr.close_all()
    
    # Launch the app
    # debug=True allows you to see errors in the terminal
    # inline=False ensures it opens in a new browser tab
    demo.queue().launch(debug=True, inline=False)
