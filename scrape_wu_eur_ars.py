import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import openpyxl
from pathlib import Path

OUTPUT_FILE = "wu_eur_ars.xlsx"
URL = "https://www.westernunion.com/es/es/currency-converter/eur-to-ars-rate.html"

async def fetch_rate():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(URL, timeout=60000)

        # Esperar a que aparezca el texto con la cotización
        await page.wait_for_selector("text=EUR =")

        # Buscar el texto del tipo "1 EUR = 1592.0365 ARS"
        text = await page.inner_text("text=EUR =")
        await browser.close()
        return text

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
