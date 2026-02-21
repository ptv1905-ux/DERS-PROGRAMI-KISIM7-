from fastapi import FastAPI, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import Annotated
import json, os, time

app = FastAPI()
security = HTTPBasic()
DB_FILE = "dersler.json"

ADMIN_USER = "admin"
ADMIN_PASS = "1234" 
def get_admin(credentials: HTTPBasicCredentials = Depends(security)):
if credentials.username != ADMIN_USER or credentials.password != ADMIN_PASS:
raise HTTPException(status_code=401, detail="Hatalı giriş!")
return credentials.username

def veri_oku():
if os.path.exists(DB_FILE):
try:
with open(DB_FILE, "r", encoding="utf-8") as f:
return json.load(f)
except: return []
return []

def veri_yaz(dersler):
with open(DB_FILE, "w", encoding="utf-8") as f:
json.dump(dersler, f, indent=4, ensure_ascii=False)
@app.get("/", response_class=HTMLResponse)
def home():
dersler = veri_oku()
satirlar = "".join([f"<tr><td>{d['gun']}</td><td>{d['saat']}</td><td>{d['ders']}</td><td>{d['hoca']}</td></tr>" for d in dersler])
return f"""<html><head><meta name="viewport" content="width=device-width, initial-scale=1.0"><style>body{{font-family:sans-serif; padding:20px; background:#f4f7f6; text-align:center;}} .box{{max-width:800px; margin:auto; background:white; padding:20px; border-radius:10px; box-shadow:0 2px 10px rgba(0,0,0,0.1);}} table{{width:100%; border-collapse:collapse;}} th,td{{padding:12px; border:1px solid #ddd;}} th{{background:#007bff; color:white;}}</style></head><body><div class="box"><h1>Ders Programi</h1><table><tr><th>GUN</th><th>SAAT</th><th>DERS</th><th>HOCA</th></tr>{satirlar if satirlar else "<tr><td colspan='4'>Ders yok.</td></tr>"}</table>


<a href="/admin" style="color:#ccc; text-decoration:none; font-size:10px;">Giris</a></div></body></html>"""
@app.get("/admin", response_class=HTMLResponse)
def admin_panel(user: str = Depends(get_admin)):
dersler = veri_oku()
satirlar = "".join([f"<tr><td>{d['gun']}</td><td>{d['saat']}</td><td>{d['ders']}</td><td>{d['hoca']}</td><td><a href='/sil/{d['id']}' style='color:red;'>Sil</a></td></tr>" for d in dersler])
return f"""<html><body style="font-family:sans-serif; padding:20px;"><h1>Yonetici Paneli</h1><form action="/ekle" method="post" style="background:#eee; padding:15px;"><input name="gun" placeholder="Gun"><input name="saat" placeholder="Saat"><input name="ders" placeholder="Ders"><input name="hoca" placeholder="Hoca"><button type="submit">Ekle</button></form><table border="1" style="width:100%; border-collapse:collapse; margin-top:20px;"><tr><th>Gun</th><th>Saat</th><th>Ders</th><th>Hoca</th><th>Islem</th></tr>{satirlar}</table></body></html>"""

@app.post("/ekle")
def ekle(gun:Annotated[str, Form()], saat:Annotated[str, Form()], ders:Annotated[str, Form()], hoca:Annotated[str, Form()], user: str = Depends(get_admin)):
mevcut = veri_oku()
mevcut.append({"id": int(time.time()), "gun": gun, "saat": saat, "ders": ders, "hoca": hoca})
veri_yaz(mevcut)
return RedirectResponse("/admin", 303)

@app.get("/sil/{id}")
def sil(id: int, user: str = Depends(get_admin)):
mevcut = [d for d in veri_oku() if d["id"] != id]
veri_yaz(mevcut)
return RedirectResponse("/admin", 303)

if name == "main":
import uvicorn
import os
port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
