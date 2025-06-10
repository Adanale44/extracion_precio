from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configurar Selenium (modo headless)
options = Options()
options.add_argument("--headless")          # No abre ventana
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
driver = webdriver.Chrome(options=options)

# URL de la categoría "Leches"
url = "https://diaonline.supermercadosdia.com.ar/frescos/leches"
driver.get(url)

# Esperar que cargue el contenido dinámico
time.sleep(10)

# Analizar el contenido HTML renderizado
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Buscar los productos
productos = soup.find_all("div", class_="diaio-search-result-0-x-galleryItem diaio-search-result-0-x-galleryItem--normal diaio-search-result-0-x-galleryItem--default pa4")

# Lista para guardar los datos
datos = []

for producto in productos:
    # Nombre
    nombre_tag = producto.find("span", class_="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Nombre no disponible"
    
    # Precio
    precio_tag = producto.find("span", class_="diaio-store-5-x-sellingPriceValue")
    precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"
    
    # Enlace
    enlace_tag = producto.find("a", class_="vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--shelf h-100 flex flex-column")
    enlace = "https://diaonline.supermercadosdia.com.ar" + enlace_tag['href'] if enlace_tag else "URL no disponible"
    
    datos.append({
        "Supermercado": "DIA",
        "Producto": nombre,
        "Precio": precio,
        "URL": enlace
    })

# Crear DataFrame y guardar como CSV
df = pd.DataFrame(datos)
df.to_csv("productos_leches_dia.csv", index=False, encoding="utf-8")
print("Extracción completada. Guardado en 'productos_leches_dia.csv'")
