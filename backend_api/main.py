from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

conn = sqlite3.connect("fitpro.db", check_same_thread=False)
cursor = conn.cursor()

# ================= BANCO =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT,
    tipo TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS treinos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    nome TEXT,
    exercicio TEXT,
    carga TEXT
)
""")

conn.commit()

# ================= MODELOS =================
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str
    tipo: str  # aluno / professor / admin

# ================= ROTAS =================
@app.post("/register")
def register(user: Usuario):
    cursor.execute("INSERT INTO usuarios (nome, email, senha, tipo) VALUES (?, ?, ?, ?)",
                   (user.nome, user.email, user.senha, user.tipo))
    conn.commit()
    return {"msg": "Usuário criado"}

@app.post("/login")
def login(email: str, senha: str):
    cursor.execute("SELECT * FROM usuarios WHERE email=? AND senha=?", (email, senha))
    user = cursor.fetchone()

    if user:
        return {"status": "ok", "user_id": user[0]}
    return {"status": "erro"}

@app.get("/treinos/{user_id}")
def get_treinos(user_id: int):
    cursor.execute("SELECT * FROM treinos WHERE usuario_id=?", (user_id,))
    return cursor.fetchall()