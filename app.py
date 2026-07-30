from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

DB_FILE = 'youtube_posts.json'

def carregar():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f:
            return json.load(f)
    return []

def salvar(dados):
    with open(DB_FILE, 'w') as f:
        json.dump(dados, f)

@app.route('/', methods=['GET'])
def home():
    return jsonify({
        "api": "Clipador - YouTube Post",
        "versao": "1.0.0",
        "categorias": ["22", "27", "28"]
    })

@app.route('/api/youtube/post', methods=['POST'])
def postar():
    data = request.json
    posts = carregar()
    
    post = {
        "id": len(posts) + 1,
        "videoUrl": data.get('videoUrl'),
        "titulo": data.get('titulo', ''),
        "descricao": data.get('descricao', ''),
        "tags": data.get('tags', []),
        "categoria": data.get('categoria', '22'),
        "privacidade": data.get('privacidade', 'public'),
        "status": "pendente",
        "criado_em": str(datetime.now())
    }
    posts.append(post)
    salvar(posts)
    
    return jsonify({
        "status": "Post agendado no YouTube!",
        "post": post
    }), 201

@app.route('/api/youtube/posts', methods=['GET'])
def listar():
    return jsonify(carregar())

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5007))
    app.run(host='0.0.0.0', port=port)