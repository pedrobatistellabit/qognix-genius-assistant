from flask import Blueprint, request, jsonify
import json
import os
from openai import OpenAI

whatsapp_bp = Blueprint('whatsapp', __name__)

# Inicializar cliente OpenAI
client = OpenAI()

def generate_creative_response(message_text, user_phone):
    """Gera resposta criativa baseada na mensagem do usuário"""
    
    # Contexto do assistente
    system_prompt = """
    Você é o Qognix Genius, um assistente de IA criativo e proativo que ajuda com:
    
    1. GERAÇÃO DE CONTEÚDO CRIATIVO:
    - Posts para Instagram, Facebook e WhatsApp
    - Textos persuasivos e criativos
    - Ideias para campanhas e projetos
    - Hashtags relevantes e engajadoras
    
    2. ANÁLISE E SUGESTÕES PROATIVAS:
    - Otimização de agenda e produtividade
    - Conselhos financeiros personalizados
    - Insights sobre tendências e oportunidades
    
    3. AUTOMAÇÃO INTELIGENTE:
    - Organização de tarefas
    - Lembretes personalizados
    - Resumos e análises
    
    Seja criativo, proativo e sempre ofereça valor adicional. Use emojis quando apropriado.
    Responda de forma natural e conversacional, como um assistente pessoal experiente.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message_text}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"✨ Desculpe, estou processando muitas solicitações no momento. Tente novamente em alguns segundos! 🤖"

def detect_intent_and_generate_response(message_text, user_phone):
    """Detecta a intenção da mensagem e gera resposta apropriada"""
    
    message_lower = message_text.lower()
    
    # Respostas específicas para diferentes tipos de solicitação
    if any(word in message_lower for word in ['post', 'instagram', 'facebook', 'rede social', 'conteúdo']):
        return generate_social_media_post(message_text)
    
    elif any(word in message_lower for word in ['agenda', 'compromisso', 'reunião', 'horário']):
        return generate_schedule_optimization(message_text)
    
    elif any(word in message_lower for word in ['ideia', 'criativo', 'brainstorm', 'sugestão']):
        return generate_creative_ideas(message_text)
    
    elif any(word in message_lower for word in ['financ', 'dinheiro', 'gasto', 'economia', 'investimento']):
        return generate_financial_advice(message_text)
    
    else:
        return generate_creative_response(message_text, user_phone)

def generate_social_media_post(context):
    """Gera post criativo para redes sociais"""
    
    prompt = f"""
    Com base no contexto: "{context}"
    
    Crie um post criativo e engajador para redes sociais que inclua:
    1. Texto principal atrativo (2-3 frases)
    2. Call-to-action envolvente
    3. 5-8 hashtags relevantes
    4. Emojis apropriados
    
    O tom deve ser inspirador e motivacional.
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.8
        )
        
        return f"📱 **POST CRIATIVO GERADO:**\n\n{response.choices[0].message.content}"
        
    except Exception as e:
        return "📱 Vou criar um post incrível para você! Aguarde um momento enquanto processo sua solicitação..."

def generate_schedule_optimization(context):
    """Gera sugestões de otimização de agenda"""
    
    suggestions = [
        "📅 **OTIMIZAÇÃO DE AGENDA:**\n\n• Bloqueie 2h pela manhã para tarefas de alta prioridade\n• Reserve 30min após o almoço para planejamento\n• Agrupe reuniões similares no mesmo período\n• Deixe 15min de buffer entre compromissos",
        
        "📅 **DICAS DE PRODUTIVIDADE:**\n\n• Use a técnica Pomodoro (25min foco + 5min pausa)\n• Defina apenas 3 prioridades por dia\n• Revise sua agenda toda noite\n• Bloqueie tempo para responder e-mails",
        
        "📅 **SUGESTÃO PERSONALIZADA:**\n\n• Manhã: Tarefas criativas (9h-11h)\n• Tarde: Reuniões e calls (14h-17h)\n• Final do dia: Planejamento do próximo dia\n• Pausas estratégicas a cada 90 minutos"
    ]
    
    import random
    return random.choice(suggestions)

def generate_creative_ideas(context):
    """Gera ideias criativas"""
    
    prompt = f"""
    Com base no contexto: "{context}"
    
    Gere 5 ideias criativas e inovadoras. Para cada ideia, forneça:
    1. Título da ideia
    2. Breve descrição (1-2 frases)
    3. Como implementar
    
    Seja criativo e pense fora da caixa!
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.9
        )
        
        return f"💡 **IDEIAS CRIATIVAS:**\n\n{response.choices[0].message.content}"
        
    except Exception as e:
        return "💡 Estou gerando ideias incríveis para você! Aqui estão algumas sugestões iniciais:\n\n• Campanha de storytelling pessoal\n• Workshop interativo online\n• Série de conteúdo educativo\n• Parceria estratégica com influenciadores\n• Challenge de engajamento de 30 dias"

def generate_financial_advice(context):
    """Gera conselhos financeiros"""
    
    advice_options = [
        "💰 **ANÁLISE FINANCEIRA:**\n\n• Regra 50-30-20: 50% necessidades, 30% desejos, 20% poupança\n• Crie uma reserva de emergência (6 meses de gastos)\n• Revise assinaturas mensais não utilizadas\n• Considere investimentos de baixo risco\n• Acompanhe seus gastos semanalmente",
        
        "💰 **DICAS DE ECONOMIA:**\n\n• Automatize sua poupança\n• Compare preços antes de compras grandes\n• Use aplicativos de cashback\n• Negocie contas mensais (internet, celular)\n• Invista em educação financeira",
        
        "💰 **ESTRATÉGIA DE INVESTIMENTO:**\n\n• Diversifique seus investimentos\n• Comece com valores pequenos\n• Estude antes de investir\n• Tenha objetivos claros\n• Reinvista os rendimentos"
    ]
    
    import random
    return random.choice(advice_options)

@whatsapp_bp.route('/webhook', methods=['GET'])
def verify_webhook():
    """Verificação do webhook do WhatsApp"""
    
    # Parâmetros de verificação do WhatsApp
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    # Token de verificação (deve ser configurado no WhatsApp Business API)
    VERIFY_TOKEN = "qognix_genius_webhook_token"
    
    if mode and token:
        if mode == 'subscribe' and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return 'Forbidden', 403
    
    return 'Bad Request', 400

@whatsapp_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    """Processa mensagens recebidas do WhatsApp"""
    
    try:
        data = request.get_json()
        
        # Log da mensagem recebida (para debug)
        print(f"Webhook recebido: {json.dumps(data, indent=2)}")
        
        # Verifica se há mensagens na requisição
        if 'entry' in data:
            for entry in data['entry']:
                if 'changes' in entry:
                    for change in entry['changes']:
                        if change.get('field') == 'messages':
                            value = change.get('value', {})
                            
                            # Processa mensagens recebidas
                            if 'messages' in value:
                                for message in value['messages']:
                                    process_message(message, value)
        
        return jsonify({'status': 'success'}), 200
        
    except Exception as e:
        print(f"Erro ao processar webhook: {str(e)}")
        return jsonify({'error': str(e)}), 500

def process_message(message, value):
    """Processa uma mensagem individual"""
    
    try:
        # Extrai informações da mensagem
        message_id = message.get('id')
        from_number = message.get('from')
        message_type = message.get('type')
        timestamp = message.get('timestamp')
        
        # Processa apenas mensagens de texto
        if message_type == 'text':
            message_text = message.get('text', {}).get('body', '')
            
            # Gera resposta criativa
            response_text = detect_intent_and_generate_response(message_text, from_number)
            
            # Aqui você enviaria a resposta de volta via WhatsApp Business API
            # send_whatsapp_message(from_number, response_text)
            
            # Por enquanto, apenas logamos a resposta
            print(f"Resposta gerada para {from_number}: {response_text}")
            
            # Salva a interação no banco de dados (opcional)
            save_interaction(from_number, message_text, response_text)
        
    except Exception as e:
        print(f"Erro ao processar mensagem: {str(e)}")

def save_interaction(phone_number, user_message, bot_response):
    """Salva a interação no banco de dados"""
    
    try:
        from src.models.user import db
        from datetime import datetime
        
        # Aqui você criaria um modelo para salvar as interações
        # Por enquanto, apenas logamos
        print(f"Interação salva: {phone_number} - {datetime.now()}")
        
    except Exception as e:
        print(f"Erro ao salvar interação: {str(e)}")

@whatsapp_bp.route('/send-message', methods=['POST'])
def send_message_api():
    """API para enviar mensagens via WhatsApp (para teste)"""
    
    try:
        data = request.get_json()
        phone_number = data.get('phone_number')
        message = data.get('message')
        
        if not phone_number or not message:
            return jsonify({'error': 'phone_number e message são obrigatórios'}), 400
        
        # Gera resposta criativa
        response = detect_intent_and_generate_response(message, phone_number)
        
        return jsonify({
            'status': 'success',
            'user_message': message,
            'bot_response': response,
            'phone_number': phone_number
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@whatsapp_bp.route('/generate-content', methods=['POST'])
def generate_content():
    """API para gerar conteúdo criativo"""
    
    try:
        data = request.get_json()
        content_type = data.get('type', 'general')
        context = data.get('context', '')
        
        if content_type == 'social_media':
            response = generate_social_media_post(context)
        elif content_type == 'ideas':
            response = generate_creative_ideas(context)
        elif content_type == 'schedule':
            response = generate_schedule_optimization(context)
        elif content_type == 'financial':
            response = generate_financial_advice(context)
        else:
            response = generate_creative_response(context, 'api_user')
        
        return jsonify({
            'status': 'success',
            'content': response,
            'type': content_type
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

