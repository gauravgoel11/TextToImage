import os
import time
from flask import Flask, render_template, request, jsonify
from PIL import Image
from io import BytesIO
import base64
from dotenv import load_dotenv

# Import the internal Google libraries (same as Colab)
import google.generativeai as genai
from google.genai import types

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Directory to save generated images
OUTPUT_DIR = os.path.join(app.static_folder, "generated_images")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --- Google AI Initialization ---
API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# Create client instance (same as Colab)
client = genai.Client(api_key=API_KEY)
MODEL_NAME = "gemini-2.0-flash-preview-image-generation"

print("✅ Google AI Initialized Successfully")

# --- Routes ---
@app.route("/")
def index():
    """Serves the main HTML page."""
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_image():
    """Handles image generation requests."""
    prompt = request.json.get("prompt")
    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        print(f"🎨 Generating image for: '{prompt}'")
        
        # Create contents object (same as Colab)
        contents = prompt
        
        # Generate content (same as Colab)
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=types.GenerateContentConfig(
                response_modalities=['TEXT', 'IMAGE']
            )
        )
        
        # Check if we have a valid candidate
        if not response.candidates:
            return jsonify({"error": "No response candidate found"}), 500
            
        # Process parts (same as Colab)
        image_data = None
        text_response = ""
        
        for part in response.candidates[0].content.parts:
            if part.text is not None:
                text_response += part.text + " "
            elif part.inline_data is not None:
                image_data = part.inline_data.data
                
        if not image_data:
            return jsonify({
                "error": "No image generated",
                "text": text_response.strip()
            }), 400

        # Save image to file
        timestamp = int(time.time())
        filename = f"image_{timestamp}.png"
        output_path = os.path.join(OUTPUT_DIR, filename)
        
        with open(output_path, "wb") as f:
            f.write(image_data)
            
        print(f"🖼️ Image saved to: {output_path}")
        
        return jsonify({
            "image_url": f"/static/generated_images/{filename}",
            "text": text_response.strip()
        })

    except Exception as e:
        print(f"🔴 Generation error: {str(e)}")
        return jsonify({
            "error": "Image generation failed",
            "details": str(e)
        }), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
