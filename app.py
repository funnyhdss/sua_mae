from flask import Flask, render_template, jsonify
import requests
from googletrans import Translator

app = Flask(__name__)
translator = Translator()

API_ENDPOINT = 'https://www.yomama-jokes.com/api/v1/jokes/random/'

@app.route('/')
def index():
    piada = obter_piada_traduzida()
    return render_template('index.html', piada=piada)

@app.route('/nova_piada')
def nova_piada():
    piada = obter_piada_traduzida()
    return jsonify({'piada': piada})

def obter_piada_traduzida():
    try:
        response = requests.get(API_ENDPOINT)
        response.raise_for_status()
        dados = response.json()
        piada_ingles = dados.get('joke', 'Nenhuma piada encontrada.')

        if piada_ingles.startswith("Yo mama"):
            piada_ingles = piada_ingles.replace("Yo mama", "Sua mãe", 1)

        traducao = translator.translate(piada_ingles, src='en', dest='pt')
        return traducao.text
    except requests.exceptions.RequestException as e:
        return f'Erro ao obter piada: {e}'
    except KeyError:
        return 'Erro na estrutura da API.'
    except Exception as e:
        print(e)
        return f'Erro na tradução: {e}'

#

if __name__ == '__main__':
    app.run()