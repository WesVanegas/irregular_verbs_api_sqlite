from flask import Flask, jsonify, request

app = Flask(__name__)

# Irregular verbs examples data

irregular_verbs = {
    "be": {"past": "was/were", "past_participle": "been", "examples":
           ["I am happy.", "He was here yesterday."]},
    "go": {"past": "went", "past_participle": "gone", "examples":
           ["I go to school,", "She went to the market."]},
    "eat":{"past": "ate", "past_participle": "eaten", "examples":
           ["I eat breakfast.", "He has eaten already"]}
}

@app.route('/api/verb/<string:verb>', methods=['GET'])
def get_verb(verb):
    """ Gets information about an irregular verb """
    verb_info = irregular_verbs.get(verb.lower())
    if verb_info:
        return jsonify(verb_info)
    else:
        return jsonify({"error":"Verb no found"}), 404

@app.route('/api/verbs', methods=['GET'])
def list_verbs():
    """ List of all available irregular verbs """
    return jsonify({"verbs":list(irregular_verbs.keys())})

if __name__ == '__main__':
    app.run(debug=True)
