import sqlite3
from openpyxl import Workbook
from datetime import datetime

wb = Workbook()
ws = wb.active
ws.title = "Relatório"

# Conectar ao banco de países
conn = sqlite3.connect('paises.db')
cursor = conn.cursor()
ws.append(["=== Países ==="])
cursor.execute("SELECT * FROM paises")
ws.append([desc[0] for desc in cursor.description])
for row in cursor.fetchall():
    ws.append(row)
conn.close()

# Espaço entre tabelas
ws.append([])

# Conectar ao banco de livros
conn = sqlite3.connect('livraria.db')
cursor = conn.cursor()
ws.append(["=== Livros ==="])
cursor.execute("SELECT * FROM livros")
ws.append([desc[0] for desc in cursor.description])
for row in cursor.fetchall():
    ws.append(row)
conn.close()

# Espaço final com nome e data
ws.append([])
ws.append(["Autor:", "Seu Nome Aqui"])
ws.append(["Data de geração:", datetime.now().strftime("%d/%m/%Y %H:%M")])

# Salvar o arquivo Excel
wb.save("relatorio_final.xlsx")
print("✅ Relatório gerado com sucesso!")
