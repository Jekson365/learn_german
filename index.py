from flask import Flask, request, jsonify, g, send_file
from flask_cors import CORS
from gtts import gTTS
import sqlite3
from objects.category import Category
from objects.sound import Sound
import os


app = Flask(__name__)
CORS(app)

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
    meaning = request.json.get('meaning')
    db = get_db()
    cursor = db.cursor()
    try:

        cursor.execute(f'INSERT INTO sounds (text,category_id,meaning) VALUES ("{text}","{category_id}","{meaning}")')
        db.commit()
        cursor.close()

        # save sound

        sound = gTTS(text=text, lang='de', slow=True)
        sound.save(f'./sounds/{text}.mp3')

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
        result.append(Category(cat[1],cat[0]).to_dict())
    db.commit()
    cursor.close()
    return jsonify({'categories':result})
@app.route("/sounds/<catid>",methods=['GET'])
def get_sounds(catid):
    db = get_db()
    cursor = db.cursor()
    result = []
    sounds = cursor.execute(f'SELECT * FROM sounds WHERE category_id="{catid}"').fetchall()
    for sound in sounds:
        obj = Sound(sound[0],sound[1],sound[2],sound[3]).to_dict()
        result.append(obj)

    db.commit()
    cursor.close()
    return {"sounds":result}
@app.route("/sound/<filename>",methods=['GET'])
def get_sound(filename):
    print(filename)
    db = get_db()
    cursor = db.cursor()
    result = cursor.execute(f'SELECT * FROM sounds where text = "{filename}"').fetchall()
    print(result)
    return send_file(f'./sounds/{result[0][1]}.mp3')

if __name__ == "__main__":
    app.run(debug=True)