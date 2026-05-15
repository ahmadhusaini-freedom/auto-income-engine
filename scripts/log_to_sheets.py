"""
Agen #5: Dashboard Tracker
Auto-log semua aktivitas ke Google Sheets
Spreadsheet jadi dashboard income real-time
Setup: buat Google Sheet, enable API, download credentials.json
"""

import os
import json
import datetime
import base64

def setup_google_sheets():
    """Setup Google Sheets client dari credentials secret"""
    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
        
        # Decode credentials dari GitHub Secret
        creds_json = os.environ.get("GOOGLE_SHEETS_CREDENTIALS", "")
        if not creds_json:
            print("[Sheets Agent] ⚠ Credentials tidak ditemukan, skip logging")
            return None
        
        creds_data = json.loads(base64.b64decode(creds_json))
        
        scopes = ["https://www.googleapis.com/auth/spreadsheets"]
        creds = Credentials.from_service_account_info(creds_data, scopes=scopes)
        service = build("sheets", "v4", credentials=creds)
        return service.spreadsheets()
        
    except Exception as e:
        print(f"[Sheets Agent] ⚠ Setup error: {e}")
        return None

def log_to_sheets(sheet, article_data: dict):
    """Tambah baris baru ke Google Sheets"""
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
    if not SPREADSHEET_ID:
        print("[Sheets Agent] ⚠ Spreadsheet ID tidak ditemukan")
        return
    
    today = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    article = article_data["article"]
    status = article_data["status"]
    
    row = [
        today,
        article["title"],
        article_data.get("medium_url", "—"),
        article_data.get("devto_url", "—"),
        article_data.get("hashnode_url", "—"),
        "✓" if status.get("medium") == "published" else "✗",
        "✓" if status.get("devto") == "published" else "✗",
        "✓" if status.get("hashnode") == "published" else "✗",
        article["reading_time_minutes"],
        "—",  # reads (update manual atau via API stats)
        "—",  # earnings (update saat payout)
        article_data["topic"]["niche"]
    ]
    
    body = {"values": [row]}
    sheet.values().append(
        spreadsheetId=SPREADSHEET_ID,
        range="Log!A:L",
        valueInputOption="USER_ENTERED",
        body=body
    ).execute()
    
    print(f"[Sheets Agent] ✓ Log ditambahkan: {article['title']}")

def create_sheet_headers(sheet):
    """Buat header kolom jika belum ada (jalankan 1x manual)"""
    SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID", "")
    headers = [[
        "Tanggal", "Judul Artikel", "Medium URL", "Dev.to URL", "Hashnode URL",
        "Medium", "Dev.to", "Hashnode", "Menit Baca", "Total Reads", "Earnings ($)", "Niche"
    ]]
    sheet.values().update(
        spreadsheetId=SPREADSHEET_ID,
        range="Log!A1:L1",
        valueInputOption="USER_ENTERED",
        body={"values": headers}
    ).execute()

def main():
    print("[Sheets Agent] Memulai logging ke Google Sheets...")
    
    with open("logs/today_article.json") as f:
        data = json.load(f)
    
    # Coba setup dan log
    try:
        sheet = setup_google_sheets()
        if sheet:
            log_to_sheets(sheet, data)
            print("[Sheets Agent] ✓ Dashboard ter-update")
        else:
            print("[Sheets Agent] ⚠ Skip — Google Sheets tidak dikonfigurasi")
    except Exception as e:
        print(f"[Sheets Agent] ⚠ Error: {e} — melanjutkan tanpa logging")
    
    # Selalu print summary terlepas dari Sheets
    article = data["article"]
    print("\n" + "=" * 50)
    print("RINGKASAN HARI INI:")
    print(f"  Artikel: {article['title']}")
    print(f"  Medium: {data.get('medium_url', 'belum publish')}")
    print(f"  Dev.to: {data.get('devto_url', 'belum publish')}")
    print(f"  Hashnode: {data.get('hashnode_url', 'belum publish')}")
    print("=" * 50)

if __name__ == "__main__":
    main()
