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

@app.before_request
def before_request():
    g.bd = conectar()

@app.teardown_request
def teardown_request(f):
    g.bd.close()




@app.route('/')
def exibir_entradas():
    #entradas = posts # Mock das postagens
    #entradas = posts[::-1] # Mock das postagens

   
     sql = "SELECT titulo, texto, data_criacao FROM posts ORDER BY id DESC"
     resultado = g.bd.execute(sql)

    entradas = [
    {"titulo":"Primeiro Titulo", "texto":"Primeiro", "data_criacao":"11/09/2023"},
    {"titulo":"Segundo Titulo", "texto":"Segundo", "data_criacao":"12/09/22023"}
        ]



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