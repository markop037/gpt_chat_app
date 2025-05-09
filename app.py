from flask import Flask, render_template, request, Response
import time
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="/")


def get_openai_response(user_message):
    try:
        chat_completion = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "user", "content": user_message}
            ],
            temperature=0.7,
            max_tokens=150
        )
        return chat_completion.choices[0].message.content.strip()
    except Exception as e:
        return f"[Error] {str(e)}"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "")

    def generate():
        try:
            response = get_openai_response(user_message)

            for word in response.split():
                yield f"data: {word}\n\n"
                time.sleep(0.1)

        except Exception as e:
            yield f"data: [Error] {str(e)}\n\n"

    return Response(generate(), content_type='text/event-stream')


if __name__ == "__main__":
    app.run(debug=True)