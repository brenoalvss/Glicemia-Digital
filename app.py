"""Glicemia Digital: site em Flask (Python) com HTML e CSS.

Registra a glicemia de 10 alunos (manhã e noite) em um banco SQLite.
Para rodar:  pip install flask   e depois   python app.py
"""
import os
import sqlite3
from datetime import date

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)
BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "turma.db")
N_ALUNOS = 10
BAIXA, ALTA = 70, 180  # faixas gerais e ilustrativas, em mg/dL


def conectar():
    con = sqlite3.connect(BANCO)
    con.row_factory = sqlite3.Row
    return con


def criar_tabelas():
    with conectar() as con:
        con.execute("CREATE TABLE IF NOT EXISTS alunos (id INTEGER PRIMARY KEY, nome TEXT NOT NULL DEFAULT '')")
        con.execute(
            """CREATE TABLE IF NOT EXISTS medicoes (
                   dia TEXT NOT NULL, aluno INTEGER NOT NULL,
                   manha INTEGER, noite INTEGER,
                   PRIMARY KEY (dia, aluno))"""
        )


def valor(texto):
    """Converte o texto do formulário em número válido (20 a 600) ou None."""
    try:
        n = int(texto)
    except (TypeError, ValueError):
        return None
    return n if 20 <= n <= 600 else None


def classe(v):
    if v is None:
        return None
    return "baixa" if v < BAIXA else ("alta" if v > ALTA else "ok")


def rotulo(c):
    return {"baixa": "Baixa", "ok": "Na faixa", "alta": "Alta"}.get(c, "")


def dia_valido(texto):
    try:
        return date.fromisoformat(texto).isoformat()
    except (TypeError, ValueError):
        return date.today().isoformat()


@app.route("/")
def index():
    dia = dia_valido(request.args.get("dia"))
    with conectar() as con:
        nomes = {r["id"]: r["nome"] for r in con.execute("SELECT id, nome FROM alunos")}
        med = {r["aluno"]: r for r in con.execute("SELECT * FROM medicoes WHERE dia = ?", (dia,))}

    alunos, todas = [], []
    for i in range(N_ALUNOS):
        m = med[i]["manha"] if i in med else None
        n = med[i]["noite"] if i in med else None
        lidas = [v for v in (m, n) if v is not None]
        media = round(sum(lidas) / len(lidas)) if lidas else None
        todas += lidas
        alunos.append({
            "i": i, "nome": nomes.get(i, ""), "manha": m, "noite": n,
            "cls_m": classe(m), "cls_n": classe(n),
            "media": media, "status": rotulo(classe(media)),
        })

    resumo = {
        "total": len(todas), "maximo": N_ALUNOS * 2,
        "media": round(sum(todas) / len(todas)) if todas else None,
        "baixas": sum(v < BAIXA for v in todas),
        "altas": sum(v > ALTA for v in todas),
    }
    return render_template("index.html", dia=dia, alunos=alunos, resumo=resumo,
                           salvo=request.args.get("salvo") == "1")


@app.route("/salvar", methods=["POST"])
def salvar():
    dia = dia_valido(request.form.get("dia"))
    with conectar() as con:
        for i in range(N_ALUNOS):
            nome = request.form.get(f"nome{i}", "").strip()[:60]
            manha = valor(request.form.get(f"manha{i}"))
            noite = valor(request.form.get(f"noite{i}"))
            con.execute("INSERT OR REPLACE INTO alunos (id, nome) VALUES (?, ?)", (i, nome))
            if manha is None and noite is None:
                con.execute("DELETE FROM medicoes WHERE dia = ? AND aluno = ?", (dia, i))
            else:
                con.execute("INSERT OR REPLACE INTO medicoes (dia, aluno, manha, noite) VALUES (?, ?, ?, ?)",
                            (dia, i, manha, noite))
    return redirect(url_for("index", dia=dia, salvo=1) + "#turma")


@app.route("/limpar-dia", methods=["POST"])
def limpar_dia():
    dia = dia_valido(request.form.get("dia"))
    with conectar() as con:
        con.execute("DELETE FROM medicoes WHERE dia = ?", (dia,))
    return redirect(url_for("index", dia=dia) + "#turma")


@app.route("/limpar-tudo", methods=["POST"])
def limpar_tudo():
    with conectar() as con:
        con.execute("DELETE FROM medicoes")
        con.execute("DELETE FROM alunos")
    return redirect(url_for("index") + "#turma")


criar_tabelas()

if __name__ == "__main__":
    app.run(debug=True)
