#!/usr/bin/env python
# coding: utf-8

# In[11]:


import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from urllib.parse import urljoin
from datetime import datetime  # Para obtener la fecha y hora actual

# Creamos una instancia del generador de User-Agent
ua = UserAgent()

# Creamos un DataFrame vacío con las columnas que vamos a almacenar
columns = ['Producto', 'Precio', 'Página', 'Categoria', 'Fecha de consulta']
df = pd.DataFrame(columns=columns)

# Función para obtener productos 
def get_products(url, page_number, categoria):
    headers = {
        'User-Agent': ua.random 
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200: # Si la solicitud se permite
        soup = BeautifulSoup(response.text, 'html.parser')
        fecha_consulta = datetime.now().strftime('%Y-%m-%d %H:%M:%S') 
        products = soup.find_all('h2', class_='h3 product-title')

        for product in products:
            product_name = product.get_text().strip()
            product_link = urljoin(url, product.find('a')['href'])
            price_tag = product.find_next('span', class_='price')
            price = price_tag.get_text().strip() if price_tag else 'No disponible'
            
            data = {'Producto': product_name, 'Precio': price,'Página': page_number,
                    'Categoria': categoria, 'Fecha de consulta': fecha_consulta}

            global df
            new_row = pd.DataFrame([data], columns=df.columns)
            df = pd.concat([df, new_row], ignore_index=True)

    else:
        print(f"Error al obtener la página {url}: {response.status_code}")

# Diccionario con las categorías y el número de páginas
categorias_y_paginas = { 'carnes': 9, 'pescados-y-mariscos': 12,'precocinados': 14,
                        'vegetales-y-frutas': 6,'helados-y-postres': 9}

for categoria, max_pages in categorias_y_paginas.items():
    print(f'Categoria: {categoria}')
    page_number = 1
    while page_number <= max_pages:
        print(f"Obteniendo productos de la página {page_number}...")

        # Construimos la URL de la página actual
        url = f"https://5oceanos.com/tenerife/comprar-congelados/{categoria}/page/{page_number}/"
        
        # Llamamos a la función para obtener los productos
        get_products(url, page_number, categoria)
        
        # Esperamos un tiempo aleatorio entre 2 y 5 segundos con el objetivo de simular un comportamiento humano
        time.sleep(random.uniform(2, 5))
        page_number += 1

df.to_csv('productos.csv', index=False) 


# In[ ]:




