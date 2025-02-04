import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re

# Diccionario para mapear abreviaturas de meses en español e inglés a números de mes
meses_map = {
    "ene": 1, "jan": 1,
    "feb": 2,
    "mar": 3,
    "abr": 4, "apr": 4,
    "may": 5,
    "jun": 6,
    "jul": 7,
    "ago": 8, "aug": 8,
    "sep": 9,
    "oct": 10,
    "nov": 11,
    "dic": 12, "dec": 12
}

# Rango de años a scrapear
anios = range(2010, 2025)  # Hasta el año actual

# Archivo de salida
archivo_csv = "data/resultados_quini6_completos.csv"

# Patrón para fechas con o sin punto en los meses
patron_fecha = re.compile(r"(\d{1,2})\s(\w+)\.?\s(\d{4})")

# Abrir el archivo CSV para escribir los resultados
with open(archivo_csv, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    # Escribir encabezado
    writer.writerow(["Fecha original", "Fecha estándar", "Tradicional", "La Segunda", "Revancha", "Siempre Sale"])

    for anio in anios:
        # URL específica del año
        target_url = f"https://resultados-de-loteria.com/quini-6/resultados/{anio}"
        print(f"Procesando el año {anio}...")

        try:
            # Realizar la solicitud HTTP a la página
            respuesta = requests.get(target_url)
            respuesta.raise_for_status()
            soup = BeautifulSoup(respuesta.content, "html.parser")

            # Encontrar todas las filas de la tabla de resultados
            filas = soup.find_all("tr")

            for fila in filas:
                try:
                    # Extraer la fecha del sorteo
                    fecha_tag = fila.find("a")
                    if fecha_tag:
                        dia = fecha_tag.find("strong").get_text(strip=True)
                        fecha_completa = fecha_tag.contents[-1].strip()  # Extraer texto después del <br>
                        fecha_original = f"{dia} {fecha_completa}"

                        # Normalizar y convertir la fecha a formato estándar
                        match = patron_fecha.search(fecha_completa)
                        if match:
                            dia_num, mes_str, anio_str = match.groups()
                            mes_str = mes_str.rstrip('.').lower()  # Normalizar: quitar punto y pasar a minúsculas
                            if mes_str in meses_map:
                                mes_num = meses_map[mes_str]
                            else:
                                raise ValueError(f"Mes desconocido: {mes_str}")
                            # Construir la fecha
                            fecha_dt = datetime(int(anio_str), mes_num, int(dia_num))
                            fecha_estandar = fecha_dt.strftime("%Y-%m-%d")
                        else:
                            raise ValueError(f"Formato de fecha inesperado: {fecha_completa}")
                    else:
                        continue

                    # Extraer los resultados de las diferentes categorías
                    resultados = fila.find_all("ul", class_="balls")
                    categorias = []
                    for resultado in resultados:
                        numeros = [li.get_text(strip=True) for li in resultado.find_all("li", class_="ball")]
                        categorias.append("-".join(numeros))

                    # Asegurarse de que haya resultados para todas las categorías
                    while len(categorias) < 4:
                        categorias.append("")

                    # Escribir los datos en el CSV
                    writer.writerow([fecha_original, fecha_estandar] + categorias)

                except Exception as e:
                    print(f"Error procesando fila: {e}")

        except Exception as e:
            print(f"Error procesando el año {anio}: {e}")

print(f"Scraping completo. Datos guardados en {archivo_csv}")
