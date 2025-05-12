from flask import Flask, render_template, request, Response
import time
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="/")


def get_openai_response(user_message):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150,
            stream=True
        )
        for chunk in chat_completion:
            if chunk.choices and chunk.choices[0].delta.content:
                yield f"data: {chunk.choices[0].delta.content}\n\n"
                time.sleep(0.05)
    except Exception as e:
        yield f"data: [Error] {str(e)}\n\n"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    return Response(get_openai_response(user_message), content_type='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)
