# Western Union EUR→ARS scraper (Excel)

Este proyecto guarda dos veces por día la cotización **EUR → ARS** publicada en la página pública de Western Union y la agrega a un archivo **Excel** (`wu_eur_ars.xlsx`) con columnas:

- Fecha (YYYY-MM-DD)
- Hora (HH:MM:SS)
- Cotización (float con 6 decimales)

## Probar localmente
1. Requisitos: Python 3.10+
2. Instalar dependencias:
   ```bash
   pip install -r requirements.txt
   ```
3. Ejecutar:
   ```bash
   python scrape_wu_eur_ars.py
   ```
4. Se generará/actualizará `wu_eur_ars.xlsx` en el directorio actual.

## Despliegue gratis con GitHub Actions
1. Crear un repositorio en GitHub.
2. Subir estos archivos:
   - `scrape_wu_eur_ars.py`
   - `requirements.txt`
   - `.github/workflows/scrape.yml`
3. GitHub Actions ejecutará el script **dos veces por día** (12:00 y 18:00 hora de Córdoba, AR).

Cada ejecución agrega una nueva fila al Excel y hace commit en el repo.

---

Hecho para mantener un histórico sencillo de la cotización EUR→ARS de Western Union.
