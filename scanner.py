import requests
import pandas as pd
import gspread

from oauth2client.service_account import (
    ServiceAccountCredentials
)

# =====================================================
# TICKERS
# =====================================================

TICKERS = [
    "AAPL",
    "TSLA",
    "NVDA",
    "AMD",
    "META",
    "AMZN"
]

# =====================================================
# GOOGLE SHEETS AUTH
# =====================================================

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]

creds = ServiceAccountCredentials.from_json_keyfile_name(
    "credenciales.json",
    scope
)

client = gspread.authorize(creds)

# =====================================================
# ABRIR GOOGLE SHEET
# =====================================================

sheet = client.open(
    "Scanner Nasdaq"
).sheet1

# =====================================================
# RESULTADOS
# =====================================================

resultados = []

# =====================================================
# HEADERS
# IMPORTANTE PARA YAHOO
# =====================================================

headers = {
    "User-Agent":
    "Mozilla/5.0"
}

# =====================================================
# RECORRER TICKERS
# =====================================================

for ticker in TICKERS:

    try:

        url = (
            f"https://query1.finance.yahoo.com/"
            f"v8/finance/chart/{ticker}"
            f"?interval=15m"
            f"&range=5d"
            f"&includePrePost=true"
        )

        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        print(
            f"{ticker} -> "
            f"Status: {response.status_code}"
        )

        # =============================================
        # VALIDAR RESPUESTA
        # =============================================

        if response.status_code != 200:

            resultados.append([
                ticker,
                "ERROR HTTP"
            ])

            continue

        data = response.json()

        # =============================================
        # VALIDAR JSON
        # =============================================

        if (
            "chart" not in data or
            not data["chart"]["result"]
        ):

            resultados.append([
                ticker,
                "SIN DATOS"
            ])

            continue

        # =============================================
        # TODO OK
        # =============================================

        resultados.append([
            ticker,
            "OK"
        ])

    except Exception as e:

        resultados.append([
            ticker,
            f"ERROR: {str(e)}"
        ])

# =====================================================
# LIMPIAR SHEET
# =====================================================

sheet.clear()

# =====================================================
# HEADERS SHEET
# =====================================================

sheet.append_row([
    "Ticker",
    "Estado"
])

# =====================================================
# ESCRIBIR RESULTADOS
# =====================================================

sheet.append_rows(resultados)

print("Proceso terminado")