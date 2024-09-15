from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


# Irregular verbs examples data
irregular_verbs = {
    "be": {"past": "was/were", "past_participle": "been", "examples":
           ["I am happy.", "He was here yesterday."]},
    "go": {"past": "went", "past_participle": "gone", "examples":
           ["I go to school,", "She went to the market."]},
    "eat":{"past": "ate", "past_participle": "eaten", "examples":
           ["I eat breakfast.", "He has eaten already"]}
}

class Verb(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    verb = db.Column(db.String(20), primary_key=True)
    past = db.Column(db.String(20), nullable=False)
    past_participle = db.Column(db.String(20), nullable=False)
    example_one = db.Column(db.String(120), nullable=False)
    example_two = db.Column(db.String(120))


@app.route('/api/verbs/add', methods=['POST'])
def add_verb():
    data = request.get_json()
    new_verb = Verb(verb=data['verb'], past=data['past'], past_participle=data['past_participle'],
                    example_one=data['example_one'], example_two=data['example_two'])
    db.session.add(new_verb)
    db.session.commit()
    return jsonify({'message': 'Verb added succesfully!'}), 201

@app.route('/api/verbs', methods=['GET'])
def list_verbs():
    verbs = Verb.query.all()
    output = []
    for verb in verbs:
        output.append({'verb': verb.verb, 'past': verb.past, 'past_participle': verb.past_participle,
                       'example_one': verb.example_one, 'example_two': verb.example_two})
    return jsonify(output)


@app.route('/api/verb/<string:verb>', methods=['GET'])
def get_verb(verb):
    verb_detail = Verb.query.get(verb)
    if verb_detail:
        return jsonify({'verb': verb_detail.verb, 'past': verb_detail.past, 'past_participle': verb_detail.past_participle, 'example_one': verb_detail.example_one, 'example_two': verb_detail.example_two})
    else:
        return jsonify({'message': 'Verb not found'}), 404



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
