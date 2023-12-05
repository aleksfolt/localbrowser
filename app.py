from flask import Flask, render_template, request, jsonify
import json

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


try:
    with open('data.json', 'r', encoding='utf-8') as file:
        json_data = json.load(file)
except FileNotFoundError:
    json_data = {"queries": []}


def search_json(query):
    matching_answers = []

    # First, search for exact matches in queries
    for item in json_data["queries"]:
        if any(q.lower() == query.lower() for q in item["queries"]):
            matching_answers.append(''.join(item["answer"]))

    # If no exact matches found, search for words in the query within answers
    if not matching_answers:
        for item in json_data["queries"]:
            if isinstance(item["answer"], str) and any(word.lower() in item["answer"].lower() for word in query.split()):
                matching_answers.append(item["answer"])

    if matching_answers:
        return matching_answers
    else:
        return "No matching answer found."



@app.route('/process_text', methods=['POST'])
def process_text():
    if request.method == 'POST':
        data = request.get_json()
        entered_text = data.get('user_input', '')
        result = search_json(entered_text)
        print(result)
        print("Entered Text:", entered_text)
        return jsonify({'result': result})


if __name__ == '__main__':
    app.run(debug=True)
