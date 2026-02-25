from flask import Flask, render_template, request, jsonify, redirect
import sqlite3
import csv
import os

app = Flask(__name__)

# =========================
# CRIAR BANCO (SEM APAGAR DADOS)
# =========================

def criar_tabela():
    conn = sqlite3.connect("atendimentos.db")
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            numero TEXT UNIQUE,
            email TEXT,
            historico TEXT,
            tipo TEXT,
            link TEXT,
            imovel TEXT,
            data_criacao TEXT,
            canal TEXT,
            status TEXT DEFAULT 'Aguardando',
            atendimento TEXT,
            detalhes TEXT,
            atendente TEXT,
            setor TEXT
        )
    """)

    conn.commit()
    conn.close()

criar_tabela()

# =========================
# HEALTH CHECK (IMPORTANTE PARA RENDER)
# =========================

@app.route("/health")
def health():
    return "OK"

# =========================
# PÁGINA PRINCIPAL
# =========================

@app.route("/")
def home():
    return render_template("index.html")

# =========================
# LISTAR DADOS
# =========================

@app.route("/listar")
def listar():
    conn = sqlite3.connect("atendimentos.db")
    c = conn.cursor()

    c.execute("SELECT * FROM atendimentos ORDER BY id DESC")
    dados = c.fetchall()

    conn.close()

    return jsonify([
        {
            "id": row[0],
            "nome": row[1],
            "numero": row[2],
            "email": row[3],
            "historico": row[4],
            "tipo": row[5],
            "link": row[6],
            "imovel": row[7],
            "data_criacao": row[8],
            "canal": row[9],
            "status": row[10],
            "atendimento": row[11],
            "detalhes": row[12],
            "atendente": row[13],
            "setor": row[14]
        }
        for row in dados
    ])

# =========================
# ASSUMIR ATENDIMENTO
# =========================

@app.route("/assumir/<int:id>", methods=["POST"])
def assumir(id):
    data = request.get_json()

    conn = sqlite3.connect("atendimentos.db")
    c = conn.cursor()

    c.execute("""
        UPDATE atendimentos
        SET status = 'Em atendimento',
            atendente = ?
        WHERE id = ?
    """, (data.get("atendente"), id))

    conn.commit()
    conn.close()

    return jsonify({"mensagem": "Atualizado"})

# =========================
# IMPORTAR CSV
# =========================

@app.route("/importar", methods=["POST"])
def importar():
    arquivo = request.files["arquivo"]

    if not os.path.exists("uploads"):
        os.makedirs("uploads")

    caminho = os.path.join("uploads", arquivo.filename)
    arquivo.save(caminho)

    conn = sqlite3.connect("atendimentos.db")
    c = conn.cursor()

    with open(caminho, newline='', encoding="utf-8") as csvfile:
        leitor = csv.DictReader(csvfile)

        for linha in leitor:
            try:
                c.execute("""
                    INSERT INTO atendimentos (
                        nome, numero, email, historico, tipo,
                        link, imovel, data_criacao, canal,
                        status, atendimento, detalhes
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Aguardando', ?, ?)
                """, (
                    linha.get("Nome"),
                    linha.get("Número"),
                    linha.get("Email"),
                    linha.get("Histórico"),
                    linha.get("Tipo"),
                    linha.get("Link"),
                    linha.get("Imóvel"),
                    linha.get("Data de criação"),
                    linha.get("Canal"),
                    linha.get("Atendimento"),
                    linha.get("Detalhes")
                ))
            except sqlite3.IntegrityError:
                pass

    conn.commit()
    conn.close()

    return redirect("/")

# =========================
# WEBHOOK LAIS.AI
# =========================

@app.route("/webhook", methods=["POST"])
def webhook():
    dados = request.get_json()

    conn = sqlite3.connect("atendimentos.db")
    c = conn.cursor()

    try:
        c.execute("""
            INSERT INTO atendimentos (
                nome, numero, email, historico, tipo,
                link, imovel, data_criacao, canal,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 'Aguardando')
        """, (
            dados.get("nome"),
            dados.get("numero"),
            dados.get("email"),
            dados.get("historico"),
            dados.get("tipo"),
            dados.get("link"),
            dados.get("imovel"),
            dados.get("data_criacao"),
            dados.get("canal")
        ))

        conn.commit()

    except sqlite3.IntegrityError:
        pass

    conn.close()

    return jsonify({"status": "ok"})

# =========================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

