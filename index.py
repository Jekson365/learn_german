from flask import Flask, request, jsonify,g
from gtts import gTTS
import sqlite3
from objects.category import Category
import os

app = Flask(__name__)

conn = sqlite3.connect('sounds.db')

def get_db():
    db = getattr(g,'_database', None)
    if db is None:
        db = g._database = sqlite3.connect('test.db')
    return db
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g,'_database', None)
    if db is not None:
        db.close()
@app.route("/",methods=['GET'])
def main():
    return "Hello"

@app.route("/create",methods=['POST'])
def create_sound():
    text = request.json.get('text')
    category_id = request.json.get('category_id')
    db = get_db()
    cursor = db.cursor()
    try:

        cursor.execute(f'INSERT INTO numbers (text,category_id) VALUES ("{text}","{category_id}")')
        db.commit()
        cursor.close()

        # save sound

        sound = gTTS(text=text, lang='de', slow=True)

        if category_id == '1':
            sound.save(f'./verbs/{text}.mp3')
        if category_id == '2':
            sound.save(f'./numbers/{text}.mp3')
        if category_id == '3':
            sound.save(f'./nouns/{text}.mp3')
        if category_id == '4':
            sound.save(f'./combinations/{text}.mp3')


        return jsonify({'message':'saved successfully'})

    except sqlite3.IntegrityError as e:
        response = {'error': str(e)}
        return jsonify(response)

@app.route("/delete",methods=['POST'])
def delete_sound():
    text = request.json.get('text')
    db = get_db()
    db.execute(f'DELETE FROM numbers WHERE text = "{text}"')
    db.commit()
    db.close()

    os.remove(f'numbers/{text}.mp3')

    return jsonify({'message':'deleted successfully'})

@app.route('/categories',methods=['GET'])
def get_categories():
    db = get_db()
    cursor = db.cursor()
    categories = cursor.execute('SELECT * FROM category').fetchall()
    result = []
    for cat in categories:
        print(cat)
        result.append(Category(cat[1],cat[0]).to_dict())

    db.commit()
    cursor.close()
    return jsonify({'categories':result})

if __name__ == "__main__":
    app.run(debug=True)