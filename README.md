# Glicemia Digital

Site educativo sobre como a tecnologia ajuda no combate ao diabetes, com um registro da glicemia de 10 alunos (manhã e noite). Feito com **HTML, CSS e Python (Flask)**.

## Estrutura

| Caminho | Função |
|---|---|
| `app.py` | Servidor Python: rotas e banco SQLite |
| `templates/index.html` | Página HTML (Jinja) |
| `static/style.css` | Estilos (azul como cor base) |
| `docs/index.html` | Versão estática, sem Python (dados salvos só no navegador) |
| `requirements.txt` | Dependências (Flask e gunicorn) |
| `Procfile` | Comando de início para hospedagens como Render |

## Rodar no computador

```bash
pip install -r requirements.txt
python app.py
```

Abra http://127.0.0.1:5000 no navegador. O banco `turma.db` é criado sozinho.

## Publicar

**Versão estática (GitHub Pages):** em *Settings → Pages*, escolha a branch `main` e a pasta `/docs`. O site fica em `https://SEU-USUARIO.github.io/NOME-DO-REPOSITORIO/`.

**Versão Python:** o GitHub não executa Python. Use PythonAnywhere ou Render, apontando para este repositório. No Render, o comando de início é `gunicorn app:app`.

## Aviso

Glicemia é dado de saúde e o site não tem login. Use dados fictícios ou autorizados. O conteúdo é informativo e não substitui consulta médica.

## Feito pelos alunos

Alice, Breno, Cecília, Henrique, João Gabriel, João Lucas, Renan, Téo, Valentyn e Yasmin.
