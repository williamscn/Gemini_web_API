from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai  # 假设 Gemini API 有官方 Python SDK
from dotenv import load_dotenv
import os

app = Flask(__name__, static_folder='../static', static_url_path='')

# 配置 Gemini API 客户端
#env_file_path = os.path.expanduser("~/Documents/Gemini/.env")
#load_dotenv(env_file_path)
api_keys = [os.getenv("GEMINI_API_KEY"), os.getenv("GEMINI_API_KEY2")]
if not all(api_keys):
    raise ValueError("API keys are not set in environment variables.")
#print(f"API keys: {api_keys[0]}, {api_keys[1]}")
genai.configure(api_key=api_keys[0])
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')

    try:
        # 调用 Gemini API
        print(f"User message: {user_message}")
        response = model.generate_content(user_message)
        #response = model.generate_content("How does AI work?")
        print(f"Response: {response.text}")
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"reply": "Error: Unable to fetch a response."}), 500

if __name__ == '__main__':
    app.run(debug=True)
