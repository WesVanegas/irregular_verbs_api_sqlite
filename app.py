from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
db = SQLAlchemy(app)


class Verb(db.Model):
    #id = db.Column(db.Integer, primary_key=True)
    verb = db.Column(db.String(20), primary_key=True)
    past = db.Column(db.String(20), nullable=False)
    past_participle = db.Column(db.String(20), nullable=False)
    example_one = db.Column(db.String(120), nullable=False)
    example_two = db.Column(db.String(120))


@app.route('/api/verb/add', methods=['POST'])
def add_verb():
    data = request.get_json()
    new_verb = Verb(verb=data['verb'], past=data['past'], past_participle=data['past_participle'],
                    example_one=data['example_one'], example_two=data['example_two'])
    db.session.add(new_verb)
    db.session.commit()
    return jsonify({'message': 'Verb added succesfully!'}), 201

@app.route('/api/verbs/add', methods=['POST'])
def add_multiple_verbs():
    data = request.get_json()
    if not isinstance(data, list):
        return jsonify({'message': 'Request body must be a list of verbs'}), 400

    failed_verbs = []

    for item in data:
        if 'verb' in item and 'past' in item and 'past_participle' in item and 'example_one' in item:
            new_verb = Verb(verb=item['verb'], past=item['past'], past_participle=item['past_participle'],
                            example_one=item['example_one'], example_two=item['example_two'])
            try:
                db.session.add(new_verb)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                failed_verbs.append({'verb': item, 'error': str(e)})
        else:
            failed_verbs.append({'verb':item, 'error': 'Missing name or something'})

    if failed_verbs:
        return jsonify({
            'message': 'Some verbs could not be added',
            'failed_verbs': failed_verbs
        }), 400
    else:
        return jsonify({'message':'All verbs added succesfully'}), 201


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


@app.route('/api/verb/<string:verb>/delete', methods=['DELETE'])
def delete_verb(verb):
    verb_to_delete = Verb.query.filter_by(verb=verb).first()
    if verb_to_delete:
        db.session.delete(verb_to_delete)
        db.session.commit()
        return jsonify({'message': 'Verb deleted successfully!'}), 200
    else:
        return jsonify({'message': 'Verb not found'}), 404


@app.route('/api/verb/<string:verb>/update', methods=['PUT'])
def update_verb(verb):
    verb_to_update = Verb.query.get(verb)
    if verb_to_update:
        data = request.get_json()
        print(data)
        if 'verb' in data:
            verb_to_update.verb = data['verb']
        if 'past' in data:
            verb_to_update.past = data['past']
        if 'past_participle' in data:
            verb_to_update.past_participle = data['past_participle']
        if 'example_one' in data:
            verb_to_update.example_one = data['example_one']
        if 'example_two' in data:
            verb_to_update.example_two = data['example_two']
        db.session.commit()
        return jsonify({'message':'Verb updated successfully!'})
    else:
        return jsonify({'message': 'Verb not found'}), 404


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
