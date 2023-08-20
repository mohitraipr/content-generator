from flask import Flask, render_template, request
from dotenv import load_dotenv
import openai
import os
app = Flask(__name__)

# Set your OpenAI API key here
# Load environment variables from .env file
load_dotenv()

# Access your variables like this
api_key = os.getenv("api_key")
openai.api_key = api_key

# Function to generate YouTube video content
def generate_youtube_content(topic):
    try:
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"Generate a YouTube video title and description about {topic}:\n\nTitle:",
            max_tokens=1000  # Adjust max_tokens for longer descriptions
        )
        generated_text = response.choices[0].text.strip()
        return generated_text
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    generated_title = ""
    generated_description = ""

    if request.method == 'POST':
        topic = request.form['topic']
        generated_content = generate_youtube_content(topic)
        if not generated_content.startswith("Error"):
            lines = generated_content.split('\n')
            generated_title = lines[0]
            generated_description = '\n'.join(lines[2:])

    return render_template('index.html', generated_title=generated_title, generated_description=generated_description)

if __name__ == '__main__':
    app.run(debug=True)
