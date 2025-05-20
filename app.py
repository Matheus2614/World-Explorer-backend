from flask import Flask, jsonify, request # Flask, jsonify para formatar resposta, request para acessar dados da requisição
from flask_cors import CORS # Para lidar com Cross-Origin Resource Sharing
from google import genai # Biblioteca para interagir com o modelo Gemini
import os # Módulo para interagir com o sistema operacional (usaremos para variáveis de ambiente)
from dotenv import load_dotenv # Importa a função para carregar .env (se python-dotenv foi instalado)
import json

load_dotenv()

app = Flask(__name__)

CORS(app)

API_KEY = os.getenv("GOOGLE_API_KEY")
client = genai.Client(api_key=API_KEY)

def gerar_resposta(pais, assunto):
    prompt = f"""Você é especialista em cultura de países, geografia e história, você será como um professor, sua personalidade será gentil e tranquilo, mas sempre vá direto ao ponto.
    Gere um texto especifico sobre o {pais} com enfase no {assunto}. Caso não seja país ou o assunto seja de cunho sexual, odio, preconceito ou não relacionado ao suas especialidades, devolva para a pessoa voltar mais tarde com uma perguta sobre um país.
    A resposta será em formato HTML com formatação UTF 8, mas sem seção <head>, tags <body> e </body>, sem <!DOCTYPE>, sem o idioma, sem a tag da formatação. Não utilize blocos de código, markdown, nem formatação como ```html, mande apenas o conteudo, apenas o título em <h1>, os subtitulos em <h2> e o conteudo em <p>.
    """
    
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )

    # Remove blocos de markdown como ```html e ```
    conteudo = response.text.strip()

    # Remove delimitadores de bloco de código, se existirem
    if conteudo.startswith("```html"):
        conteudo = conteudo.replace("```html", "").strip()
    if conteudo.endswith("```"):
        conteudo = conteudo[:-3].strip()

    return conteudo

@app.route('/conteudo', methods=['POST'])
def make_conteudo():
    try:
        # Tenta obter os dados da requisição como JSON.
        dados = request.get_json()

        # Obtém a lista de ingredientes do JSON. Se a chave "ingredientes" não
        # existir, usa uma lista vazia como valor padrão.
        pais = dados.get('pais')
        assunto = dados.get('assunto')

        # Valida se o campo "ingredientes" é uma lista.
        if not pais and not assunto:
            return jsonify({'error': 'O campos são obrigatórios!.'}), 400

        # Chama a função criar_receita para gerar a receita com base nos ingredientes.
        response = gerar_resposta(pais, assunto)

        # Retorna a receita como JSON com o código de status 200 (OK).
        return (response), 200

    except Exception as e:
        # Se ocorrer algum erro durante o processo, imprime o erro no console
        # e retorna um JSON com a mensagem de erro e o código de status 500
        # (Internal Server Error).
        print(f"Um erro interno ocorreu na API: {e}")
        return jsonify({'error': str(e)}), 500  # Retorna código 500 para erros internos

if __name__ == '__main__':
    app.run(debug=True)
