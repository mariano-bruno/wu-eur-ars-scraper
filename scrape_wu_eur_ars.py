import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import openpyxl
from pathlib import Path
import re

OUTPUT_FILE = "wu_eur_ars.xlsx"
URL = "https://www.westernunion.com/es/es/web/send-money/start?ReceiveCountry=AR&ISOCurrency=ARS&SendAmount=100.00&FundsOut=AG&FundsIn=CreditCard"

async def fetch_rate():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL, timeout=60000)

        # Esperar hasta que aparezca algo con "EUR ="
        await page.wait_for_selector("text=EUR =")

        # Buscar el texto completo que contiene la cotización
        content = await page.content()

        # Regex: 1.00 EUR = 1,712.3015
        match = re.search(r"1\.00\s*EUR\s*=\s*([\d\.,]+)", content)
        if not match:
            raise RuntimeError("No se pudo extraer la cotización del HTML")
        rate_str = f"1.00 EUR = {match.group(1)}"
        
        await browser.close()
        return rate_str

def save_to_excel(date_str, time_str, rate_str):
    path = Path(OUTPUT_FILE)

    if path.exists():
        wb = openpyxl.load_workbook(path)
        ws = wb.active
    else:
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.append(["Fecha", "Hora", "Cotizacion"])

    ws.append([date_str, time_str, rate_str])
    wb.save(path)

async def main():
    rate_str = await fetch_rate()
    now = datetime.now()
    save_to_excel(now.date().isoformat(), now.strftime("%H:%M:%S"), rate_str)
    print(f"Guardado: {rate_str}")

if __name__ == "__main__":
    asyncio.run(main())
