from flask import Flask, request, jsonify
from twilio.rest import Client
import openai

app = Flask(__name__)

# Configura tu cuenta de Twilio
account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
client = Client(account_sid, auth_token)

def enviar_mensaje_whatsapp(numero_cliente, mensaje):
    from_whatsapp_number = 'whatsapp:+14155238886'
    to_whatsapp_number = f'whatsapp:+{numero_cliente}'
    
    message = client.messages.create(
        body=mensaje,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    return message.sid

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    mensaje_cliente = data['message']
    numero_cliente = data['phone_number']
    
    # Generar mensaje persuasivo
    mensaje_persuasivo = openai.Completion.create(
      engine="davinci",
      prompt=f"Genera un mensaje persuasivo para invitar al cliente a concretar la compra en WhatsApp. Incluye el producto del que está interesado.",
      max_tokens=150
    ).choices[0].text.strip()
    
    # Enviar mensaje por WhatsApp
    message_sid = enviar_mensaje_whatsapp(numero_cliente, mensaje_persuasivo)
    
    return jsonify({"response": f"Mensaje enviado con SID: {message_sid}"})

if __name__ == '__main__':
    app.run(port=5000)