from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configurar Selenium en modo headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# URL de la categoría "Leches"
url = "https://www.cotodigital.com.ar/sitios/cdigi/categoria/catalogo-frescos-l%C3%A1cteos-leches/_/N-zpvqr7?Nf=product.startDate%7CLTEQ%201.743984E12%7C%7Cproduct.startDate%7CLTEQ%201.7495136E12%7C%7Cproduct.endDate%7CGTEQ%201.7495136E12%7C%7Cproduct.endDate%7CGTEQ%201.743984E12&Nr=AND(product.sDisp_200:1004,product.language:espa%C3%B1ol,OR(product.siteId:CotoDigital))&Ns=product.TOTALDEVENTAS%7C1"
driver.get(url)

# Esperar que cargue todo el contenido (y si es necesario hacer scroll)
time.sleep(5)

# Obtener el contenido renderizado
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Buscar productos
productos = soup.find_all("div", class_="mt-4 col-12 col-md-9 col-lg-9 col-xxl-9 col-xl-9")

datos = []

for producto in productos:
    # Nombre del producto
    nombre_tag = producto.find("a", class_="nombre-producto cursor-pointer")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Nombre no disponible"

    # Precio del producto
    precio_tag = producto.find("div", class_="card-text d-block ng-star-inserted")
    precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"

    # URL del producto
    enlace = "https://www.cotodigital.com.ar" + nombre_tag['href'] if nombre_tag and nombre_tag.has_attr('href') else "URL no disponible"

    # Guardar en la lista
    datos.append({
        "Supermercado": "COTO",
        "Producto": nombre,
        "Precio": precio,
        "URL": enlace
    })

# Crear DataFrame y guardar en CSV
df = pd.DataFrame(datos)
df.to_csv("productos_leches_coto.csv", index=False, encoding="utf-8")
print("Extracción completada. Guardado en 'productos_leches_coto.csv'")
