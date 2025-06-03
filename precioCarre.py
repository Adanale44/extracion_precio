from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import pandas as pd
import time

# Configuración para correr Chrome en modo headless (sin abrir ventana)
options = Options()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

# Crear el navegador
driver = webdriver.Chrome(options=options)

# URL de Carrefour
url = "https://www.carrefour.com.ar/Lacteos-y-productos-frescos/Leches?order="

# Abrir la página
driver.get(url)
time.sleep(5)  # Esperar que cargue el contenido dinámico

# Extraer el HTML final
soup = BeautifulSoup(driver.page_source, "html.parser")
driver.quit()

# Buscar los productos
productos = soup.find_all("div", class_="vtex-product-summary-2-x-container")

# Almacenar los datos
datos = []
for producto in productos:
    nombre_tag = producto.find("span", class_="vtex-product-summary-2-x-productBrand")
    nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Nombre no disponible"

    precio_tag = producto.find("span", class_="vtex-product-price-1-x-currencyInteger")
    precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"

    enlace_tag = producto.find("a", class_="vtex-product-summary-2-x-clearLink")
    enlace = "https://www.carrefour.com.ar" + enlace_tag['href'] if enlace_tag else "URL no disponible"

    datos.append({
        "Supermercado": "Carrefour",
        "Producto": nombre,
        "Precio": precio,
        "URL": enlace
    })

# Guardar en CSV
df = pd.DataFrame(datos)
df.to_csv("productos_leches_carrefour.csv", index=False, encoding="utf-8")
print("Productos guardados correctamente en 'productos_leches_carrefour.csv'")
