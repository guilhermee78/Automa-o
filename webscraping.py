import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('livraria.db')
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS livros (
    titulo TEXT, preco TEXT, avaliacao TEXT, disponibilidade TEXT
)
''')

url = "https://books.toscrape.com/catalogue/page-1.html"
res = requests.get(url)
soup = BeautifulSoup(res.text, 'html.parser')

livros = soup.select('.product_pod')[:10]

for livro in livros:
    titulo = livro.h3.a['title']
    preco = livro.select_one('.price_color').text
    avaliacao = livro.p['class'][1]  # Ex: 'Three', 'Five'
    disponibilidade = livro.select_one('.availability').text.strip()

    cursor.execute('INSERT INTO livros VALUES (?, ?, ?, ?)',
                   (titulo, preco, avaliacao, disponibilidade))

conn.commit()
conn.close()
