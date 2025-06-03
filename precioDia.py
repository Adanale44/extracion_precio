import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL de la categoría "Leches" en Supermercados DIA
url = "https://diaonline.supermercadosdia.com.ar/frescos/leches"

# Encabezados para la solicitud HTTP
headers = {
    "User-Agent": "Mozilla/5.0"
}

# Realizar la solicitud HTTP
response = requests.get(url, headers=headers)

# Verificar que la solicitud fue exitosa
if response.status_code == 200:
    soup = BeautifulSoup(response.content, "html.parser")
    
    # Encontrar todos los contenedores de productos
    productos = soup.find_all("div", class_="diaio-search-result-0-x-galleryItem diaio-search-result-0-x-galleryItem--normal diaio-search-result-0-x-galleryItem--default pa4")
    
    # Lista para almacenar los datos extraídos
    datos = []
    
    for producto in productos:
        # Extraer el nombre del producto
        nombre_tag = producto.find("span", class_="vtex-product-summary-2-x-productBrand vtex-product-summary-2-x-brandName t-body")
        nombre = nombre_tag.get_text(strip=True) if nombre_tag else "Nombre no disponible"
        
        # Extraer el precio del producto
        precio_tag = producto.find("span", class_="diaio-store-5-x-sellingPrice")
        precio = precio_tag.get_text(strip=True) if precio_tag else "Precio no disponible"
        
        # Extraer la URL del producto
        enlace_tag = producto.find("a", class_="vtex-product-summary-2-x-clearLink vtex-product-summary-2-x-clearLink--shelf h-100 flex flex-column")
        enlace = "https://diaonline.supermercadosdia.com.ar" + enlace_tag['href'] if enlace_tag else "URL no disponible"
        
        # Agregar los datos a la lista
        datos.append({
            "Supermercado": "DIA",
            "Producto": nombre,
            "Precio": precio,
            "URL": enlace
        })
    
    # Crear un DataFrame con los datos
    df = pd.DataFrame(datos)
    
    # Guardar los datos en un archivo CSV
    df.to_csv("productos_leches_dia.csv", index=False, encoding="utf-8")
    
    print("Extracción completada. Datos guardados en 'productos_leches_dia.csv'.")
else:
    print(f"Error al acceder a la página. Código de estado: {response.status_code}")
