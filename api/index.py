from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/api/prever', methods=['POST'])
def prever():
    try:
        data = request.json
        payout = float(data.get("payout", 1.0))
        
        # Lógica de Decisão "Deus"
        # Se o crash anterior foi baixo, a probabilidade de subir aumenta
        status = "ENTRAR" if payout < 1.50 else "AGUARDAR"
        
        return jsonify({
            "status": status,
            "previsao": round(payout * 1.12, 2)
        })
    except:
        return jsonify({"erro": "falha"}), 400

# Necessário para a Vercel
def handler(event, context):
    return app(event, context)