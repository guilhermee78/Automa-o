import requests
import sqlite3

# Conectar (ou criar) o banco de dados
conn = sqlite3.connect('paises.db')
cursor = conn.cursor()

# Criar a tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS paises (
    nome_comum TEXT, nome_oficial TEXT, capital TEXT, continente TEXT,
    regiao TEXT, sub_regiao TEXT, populacao INTEGER, area REAL,
    moeda_nome TEXT, moeda_simbolo TEXT, idioma TEXT,
    fuso_horario TEXT, bandeira TEXT
)
''')

# Receber os nomes dos 3 países
paises = []
for i in range(3):
    pais = input(f"Digite o nome do {i+1}º país: ")
    paises.append(pais.strip())

# Buscar e salvar dados de cada país
for pais in paises:
    try:
        url = f"https://restcountries.com/v3.1/name/{pais}"
        resposta = requests.get(url)
        dados = resposta.json()[0]

        nome_comum = dados['name']['common']
        nome_oficial = dados['name']['official']
        capital = dados.get('capital', [''])[0]
        continente = dados['continents'][0]
        regiao = dados.get('region', '')
        sub_regiao = dados.get('subregion', '')
        populacao = dados.get('population', 0)
        area = dados.get('area', 0.0)

        moeda = list(dados['currencies'].values())[0]
        moeda_nome = moeda['name']
        moeda_simbolo = moeda['symbol']

        idioma = list(dados['languages'].values())[0]
        fuso = dados['timezones'][0]
        bandeira = dados['flags']['png']

        # Inserir os dados na tabela
        cursor.execute('INSERT INTO paises VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)',
                       (nome_comum, nome_oficial, capital, continente, regiao, sub_regiao,
                        populacao, area, moeda_nome, moeda_simbolo, idioma, fuso, bandeira))
        print(f"✅ Dados de '{nome_comum}' salvos com sucesso.")

    except Exception as e:
        print(f"❌ Erro ao buscar dados para '{pais}': {e}")

# Salvar e fechar
conn.commit()
conn.close()
print("📁 Dados armazenados em 'paises.db'")
