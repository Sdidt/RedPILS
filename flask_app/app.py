from flask_cors import CORS
from flask import Flask, request, url_for, jsonify
import json
app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins":"*"}})

@app.route('/')
def hello():
    return "Hello World! This is a test app"

top_kr=[{'comment': "Rahul Gandhi can never be Savarkar", 'url': "https://example.com"}, {'comment': "Pappu is UNFORTUNATELY an MP", 'url': "https://example.com"}, {'comment': "Congress should get rid of Gandhis", 'url': "https://example.com"}, {'comment': "Democracy is not a family Business", 'url': "https://example.com"}, {'comment': "Pappu becomes a joke again", 'url': "https://example.com"}]
top_kl=[{'comment': "Death of Democracy", 'url': "https://example.com"}, {'comment': "BJP silencing critics. bad sign for democracy", 'url': "https://example.com"}, {'comment': "Rahul arrest is dirty hindutwa politics", 'url': "https://example.com"}, {'comment': "Modi diverting attention from Adani Scam", 'url': "https://example.com"}, {'comment': "Rahul arrest will backfire on Modi", 'url': "https://example.com"}]



@app.route('/dummy_query', methods=["GET"])
def dummy():
    args = request.args
    query = args.get("query")
    if request.method=='GET':
        if query == "BJP" or query == "Right" or query=="Pappu":
            response =  jsonify({"query":query, "topk":top_kr})
        elif query == "Left" or query == "Rahul" or query=="Democracy":
            response = jsonify({"query":query, "topk":top_kl})
        response = jsonify({"query":query, "topk":top_kr})

        response.headers.add("Access-Control-Allow-Origin", "*")
        return response

if __name__ == "__main__":
   app.run(debug=True)