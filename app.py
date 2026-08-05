from flask import Flask, request, render_template_string
from vedic_ai_tools import vedvoice_transcription, bhagavadgpt_response

app = Flask(__name__)

TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>🕉️ ShreeVed AI – VedVoice & BhagavadGPT</title>
    <style>
        body { font-family: sans-serif; background: #f3fdf3; padding: 20px; }
        h1 { color: #3a7f3a; }
        textarea { width: 100%%; height: 100px; }
        button { background-color: #3a7f3a; color: white; padding: 10px 20px; border: none; }
    </style>
</head>
<body>
    <h1>🧘 VedVoice & BhagavadGPT</h1>
    <form method="post">
        <label>Ask a Question:</label><br>
        <textarea name="query"></textarea><br><br>
        <button type="submit">🔍 Ask Gita</button>
    </form>

    {% if response %}
        <h2>🧠 Response:</h2>
        <p>{{ response }}</p>
    {% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    response = ""
    if request.method == "POST":
        query = request.form.get("query")
        if query:
            response = bhagavadgpt_response(query)
    return render_template_string(TEMPLATE, response=response)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
