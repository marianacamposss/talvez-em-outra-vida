from flask import Flask, request, render_template  
import requests  
import json  

app = Flask(__name__)  

API_ENDPOINT = 'https://randomuser.me/api/'  



# requisição à API e retorna os dados em formato JSON
def obter_dados_api():
    try:
        resposta = requests.get(API_ENDPOINT)  # requisição GET para a API
        resposta.raise_for_status() 
        return resposta.json()  
    except requests.exceptions.RequestException as erro:
        return {"erro": f"Erro ao fazer a requisição para a API: {erro}"} 
    except json.JSONDecodeError as erro:
        return {"erro": f"Erro ao processar a resposta da API: {erro}"}  # Trata erros ao decodificar o JSON


#extrai o link da imagem a partir dos dados
def extrair_url_imagem(dados):
    try:
        return dados["results"][0]["picture"]["large"]  # Extrai o link da imagem
    except (KeyError, IndexError):  # Trata possíveis erros se a estrutura dos dados mudar
        return None  #  None se não encontrar a imagem


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET': 
        return render_template('index.html') 

    nome = request.form.get('nome', None) 
    if not nome:  # Se o nome não foi informado
        return render_template('index.html', erro="⚠ Você precisa informar um nome!") 

    dados = obter_dados_api()  # Faz a requisição pra obter os dados do usuário

    if "erro" in dados:  # erro na requisição
        return render_template('index.html', erro=dados["erro"]) 

    url_imagem = extrair_url_imagem(dados)  # Extrai o URL da imagem do rosto do usuário

    if url_imagem:  
        return render_template('index.html', nome=nome, url_imagem=url_imagem)  # Exibe a imagem e o nome
    else:  
        return render_template('index.html', erro="Erro ao obter o URL da imagem.")  # Exibe erro


if __name__ == '__main__':
    app.run(debug=True)