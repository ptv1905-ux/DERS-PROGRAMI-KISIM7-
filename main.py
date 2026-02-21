from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from typing import Annotated
import json, os, time

app = FastAPI()
DB_FILE = "dersler.json"

def veri_oku():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def veri_yaz(dersler):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(dersler, f, indent=4, ensure_ascii=False)

@app.get("/", response_class=HTMLResponse)
def home():
    dersler = veri_oku()
    satirlar = ""
    for d in dersler:
        satirlar += f"""
        <tr>
            <td>{d['gun']}</td>
            <td>{d['saat']}</td>
            <td><strong>{d['ders']}</strong></td>
            <td>{d['hoca']}</td>
            <td class='actions'>
                <a href='/duzenle/{d['id']}' class='btn-edit'>✏️ Düzenle</a>
                <a href='/sil/{d['id']}' class='btn-delete'>❌ Sil</a>
            </td>
        </tr>"""
    
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f0f2f5; color: #333; margin: 0; padding: 40px; }}
            .container {{ max-width: 1000px; margin: auto; background: white; padding: 30px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); }}
            h1 {{ color: #1a73e8; margin-bottom: 25px; font-weight: 600; }}
            
            form {{ display: flex; gap: 10px; margin-bottom: 30px; flex-wrap: wrap; background: #f8f9fa; padding: 20px; border-radius: 10px; }}
            input {{ padding: 12px; border: 1px solid #ddd; border-radius: 8px; flex: 1; min-width: 150px; font-size: 14px; }}
            button {{ padding: 12px 25px; background-color: #34a853; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; transition: 0.3s; }}
            button:hover {{ background-color: #2d8e47; transform: translateY(-2px); }}

            table {{ width: 100%; border-collapse: collapse; margin-top: 10px; }}
            th {{ background-color: #1a73e8; color: white; text-align: left; padding: 15px; font-size: 15px; }}
            td {{ padding: 15px; border-bottom: 1px solid #eee; font-size: 14px; }}
            tr:hover {{ background-color: #f8f9fa; }}
            
            .actions {{ display: flex; gap: 10px; }}
            .btn-edit {{ text-decoration: none; color: #1a73e8; background: #e8f0fe; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 500; }}
            .btn-delete {{ text-decoration: none; color: #d93025; background: #feeaee; padding: 6px 12px; border-radius: 6px; font-size: 13px; font-weight: 500; }}
            .btn-edit:hover {{ background: #d2e3fc; }}
            .btn-delete:hover {{ background: #fad2cf; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🗓️ Ders Programı Yönetimi</h1>
            
            <form action="/ekle" method="post">
                <input name="gun" placeholder="Gün (Pazartesi...)" required>
                <input name="saat" placeholder="Saat (09:00)" required>
                <input name="ders" placeholder="Ders Adı" required>
                <input name="hoca" placeholder="Hoca Adı" required>
                <button type="submit">➕ Yeni Ders Ekle</button>
            </form>

            <table>
                <thead>
                    <tr>
                        <th>GÜN</th>
                        <th>SAAT</th>
                        <th>DERS</th>
                        <th>HOCA</th>
                        <th>İŞLEMLER</th>
                    </tr>
                </thead>
                <tbody>
                    {satirlar if satirlar else "<tr><td colspan='5' style='text-align:center; color:#888;'>Henüz ders eklenmedi. Başlamak için yukarıdaki formu kullanın.</td></tr>"}
                </tbody>
            </table>
        </div>
    </body>
    </html>
    """

@app.post("/ekle")
def ekle(gun:Annotated[str, Form()], saat:Annotated[str, Form()], ders:Annotated[str, Form()], hoca:Annotated[str, Form()]):
    mevcut = veri_oku()
    mevcut.append({"id": int(time.time()), "gun": gun, "saat": saat, "ders": ders, "hoca": hoca})
    veri_yaz(mevcut)
    return RedirectResponse("/", 303)

@app.get("/duzenle/{id}", response_class=HTMLResponse)
def edit_page(id: int):
    dersler = veri_oku()
    d = next((x for x in dersler if x["id"] == id), None)
    if not d: return RedirectResponse("/")
    
    return f"""
    <html>
    <head>
        <style>
            body {{ font-family: sans-serif; background: #f0f2f5; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }}
            .edit-box {{ background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); width: 400px; }}
            h2 {{ color: #1a73e8; margin-top: 0; }}
            input {{ width: 100%; padding: 12px; margin: 10px 0; border: 1px solid #ddd; border-radius: 8px; box-sizing: border-box; }}
            .save-btn {{ width: 100%; padding: 12px; background: #1a73e8; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; margin-top: 10px; }}
            .cancel-btn {{ display: block; text-align: center; margin-top: 15px; color: #666; text-decoration: none; font-size: 14px; }}
        </style>
    </head>
    <body>
        <div class="edit-box">
            <h2>✏️ Dersi Güncelle</h2>
            <form action="/guncelle/{id}" method="post" style="display:block; background:none; padding:0;">
                <label>Gün:</label><input name="gun" value="{d['gun']}">
                <label>Saat:</label><input name="saat" value="{d['saat']}">
                <label>Ders:</label><input name="ders" value="{d['ders']}">
                <label>Hoca:</label><input name="hoca" value="{d['hoca']}">
                <button type="submit" class="save-btn">💾 Değişiklikleri Kaydet</button>
                <a href="/" class="cancel-btn">Vazgeç</a>
            </form>
        </div>
    </body>
    </html>
    """

@app.post("/guncelle/{id}")
def guncelle(id:int, gun:Annotated[str, Form()], saat:Annotated[str, Form()], ders:Annotated[str, Form()], hoca:Annotated[str, Form()]):
    mevcut = veri_oku()
    for d in mevcut:
        if d["id"] == id:
            d["gun"], d["saat"], d["ders"], d["hoca"] = gun, saat, ders, hoca
    veri_yaz(mevcut)
    return RedirectResponse("/", 303)

@app.get("/sil/{id}")
def sil(id: int):
    mevcut = [d for d in veri_oku() if d["id"] != id]
    veri_yaz(mevcut)
    return RedirectResponse("/", 303)
if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)