import sqlite3

conn = sqlite3.connect("atendimentos.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS atendimentos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome_cliente TEXT,
    telefone TEXT,
    setor TEXT,
    status TEXT,
    atendente TEXT,
    hora_inicio TEXT,
    hora_fim TEXT
)
""")

conn.commit()
conn.close()

print("Banco criado com sucesso!")
