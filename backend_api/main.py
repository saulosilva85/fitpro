from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3

# ================= APP =================
app = FastAPI()

# 🔥 CORS (libera acesso do app/celular/web)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # em produção, limitar domínio
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ================= BANCO =================
conn = sqlite3.connect("fitpro.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    email TEXT,
    senha TEXT,
    peso TEXT,
    objetivo TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS exercicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT,
    series TEXT,
    reps TEXT,
    peso TEXT
)
""")

conn.commit()

# ================= MODELOS =================
class Usuario(BaseModel):
    nome: str
    email: str
    senha: str
    peso: str
    objetivo: str

# ================= ROTAS =================

# 🔥 ROTA RAIZ (CORRIGE 404)
@app.get("/")
def home():
    return {"msg": "API FitPro rodando 🚀"}


# 🔐 Cadastro
@app.post("/register")
def register(user: Usuario):
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, peso, objetivo) VALUES (?, ?, ?, ?, ?)",
        (user.nome, user.email, user.senha, user.peso, user.objetivo)
    )
    conn.commit()
    return {"status": "ok", "msg": "Usuário cadastrado"}


# 🔐 Login
@app.post("/login")
def login(email: str, senha: str):
    cursor.execute(
        "SELECT * FROM usuarios WHERE email=? AND senha=?",
        (email, senha)
    )
    user = cursor.fetchone()

    if user:
        return {"status": "ok", "user_id": user[0]}
    else:
        return {"status": "erro", "msg": "Login inválido"}


# 🏋️ Listar exercícios
@app.get("/exercicios")
def listar_exercicios():
    cursor.execute("SELECT * FROM exercicios")
    return cursor.fetchall()


# ➕ Adicionar exercício
@app.post("/exercicios")
def adicionar_exercicio(nome: str, series: str, reps: str, peso: str):
    cursor.execute(
        "INSERT INTO exercicios (nome, series, reps, peso) VALUES (?, ?, ?, ?)",
        (nome, series, reps, peso)
    )
    conn.commit()
    return {"status": "ok"}


# ❌ Deletar exercício
@app.delete("/exercicios/{id}")
def deletar_exercicio(id: int):
    cursor.execute("DELETE FROM exercicios WHERE id=?", (id,))
    conn.commit()
    return {"status": "ok"}