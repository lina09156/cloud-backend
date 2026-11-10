# файл app.py - положен в корень репозитория cloud-backend
import os
from flask import Flask, jsonify, request
from flask_cors import CORS
from supabase import create_client
 
app = Flask(__name__)
CORS(app)  # разрешаем запросы с другого домена (GitHub Pages)
app.json.ensure_ascii = False  # чтобы русский текст в ответах был читаемым
 
# ТВОИ ДАННЫЕ SUPABASE (вставлены напрямую)
SUPABASE_URL = os.environ.get("SUPABASE_URL", "https://nedwvthcrdalnljuxqxn.supabase.co")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY", "sb_publishable_g6gSs011FB_CxED2C-ZYWA_3T7KTmNC")
 
supabase = None
if SUPABASE_URL and SUPABASE_KEY:
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
 
 
@app.get("/")
def home():
    return jsonify({"status": "ok", "message": "Бэкенд работает"})
 
 
@app.get("/stats")
def stats():
    # Считаем, сколько всего задач в таблице tasks
    if supabase is None:
        return jsonify({"error": "Supabase не настроен"}), 500
    result = supabase.table("tasks").select("id", count="exact").execute()
    return jsonify({"total_tasks": result.count})
 
 
@app.post("/echo")
def echo():
    data = request.get_json(silent=True) or {}
    return jsonify({"you_sent": data})
 
 
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))