from flask import Flask, render_template, request, session, flash, redirect, url_for
from flask import Flask, render_template, request, session, abort, flash, redirect, url_for
from posts import posts
import sqlite3

app = Flask(__name__)
app.config['SECRET_KEY'] = 'pudim'

app.config.from_object(_name_)

DATABASE = "banco.bd"

def conectar ():
    return sqlite3.connect(DATABASE)

posts = [
    {
        "titulo": "Minha primeira postagem",
        "texto": "teste"
    },
    {
        "titulo": "Segundo Post",
        'texto': "outro teste"
    }
]

@app.route('/')
def exibir_entradas():
    entradas = posts # Mock das postagens
    entradas = posts[::-1] # Mock das postagens
    return render_template('exibir_entradas.html', entradas=entradas)

@app.route('/login', methods=["GET", "POST"])
@@ -29,3 +19,28 @@ def login():
            return redirect(url_for('exibir_entradas'))
        erro = "Usuário ou senha inválidos"        
    return render_template('login.html', erro=erro)

@app.route('/logout')
def logout():
    session.pop('logado')
    flash('Logout efetuado com sucesso!')
    return redirect(url_for('exibir_entradas'))

@app.route('/inserir', methods=["POST"])
def inserir_entradas():
    if session['logado']:
        novo_post = {
            "titulo": request.form['titulo'],
            "texto": request.form['texto']
        }
        posts.append(novo_post)
        flash("Post criado com sucesso!")
    return redirect(url_for('exibir_entradas'))

@app.route('/posts/<int:id>')
def exibir_entrada(id):
    try:
        entrada = posts[id-1]
        return render_template('exibir_entrada.html', entrada=entrada)
    except Exception:
        return abort(404)