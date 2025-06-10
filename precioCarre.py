from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configuración de Selenium
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# URL de la categoría Leches en Carrefour
url = "https://www.carrefour.com.ar/Lacteos-y-productos-frescos/Leches?order="
driver.get(url)
time.sleep(6)  # Esperar a que cargue el contenido

# Scroll para cargar más productos (si es necesario)
for _ in range(3):  # Se puede ajustar para cargar más
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# Analizar el contenido con BeautifulSoup
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Encontrar todos los productos
productos = soup.find_all("article", class_="pr0  vtex-flex-layout-0-x-stretchChildrenWidth   flex")

datos = []

for producto in productos:
    # Nombre del producto
    nombre_tag = producto.find("span", class_="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Nombre no disponible"

    # Precio
    precio_tag = producto.find("span", class_="vtex-flex-layout-0-x-flexColChild vtex-flex-layout-0-x-flexColChild--wrapPrice pb0")
    precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"

    # Enlace al producto
    enlace_tag = producto.find("a", class_="vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--contentProduct h-100 flex flex-column")
    enlace = "https://www.carrefour.com.ar" + enlace_tag['href'] if enlace_tag and enlace_tag.has_attr('href') else "URL no disponible"

    datos.append({
        "Supermercado": "Carrefour",
        "Producto": nombre,
        "Precio": precio,
        "URL": enlace
    })

# Crear DataFrame y guardar en CSV
df = pd.DataFrame(datos)
df.to_csv("productos_leches_carrefour.csv", index=False, encoding="utf-8")
print("✅ Extracción completada. Guardado en 'productos_leches_carrefour.csv'")