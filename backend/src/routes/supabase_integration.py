from flask import Blueprint, request, jsonify
import os
from supabase import create_client, Client
from datetime import datetime
import json

supabase_bp = Blueprint('supabase', __name__)

# Configuração do Supabase
SUPABASE_URL = os.getenv('SUPABASE_URL', 'https://your-project.supabase.co')
SUPABASE_KEY = os.getenv('SUPABASE_ANON_KEY', 'your-anon-key')

# Inicializar cliente Supabase
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

class SupabaseManager:
    """Gerenciador das operações com Supabase"""
    
    def __init__(self):
        self.supabase = supabase
    
    def save_user_interaction(self, phone_number, user_message, bot_response, interaction_type='chat'):
        """Salva interação do usuário no Supabase"""
        try:
            data = {
                'phone_number': phone_number,
                'user_message': user_message,
                'bot_response': bot_response,
                'interaction_type': interaction_type,
                'created_at': datetime.now().isoformat(),
                'metadata': {
                    'message_length': len(user_message),
                    'response_length': len(bot_response)
                }
            }
            
            result = self.supabase.table('user_interactions').insert(data).execute()
            return result.data
            
        except Exception as e:
            print(f"Erro ao salvar interação: {str(e)}")
            return None
    
    def get_user_history(self, phone_number, limit=50):
        """Recupera histórico de conversas do usuário"""
        try:
            result = self.supabase.table('user_interactions')\
                .select('*')\
                .eq('phone_number', phone_number)\
                .order('created_at', desc=True)\
                .limit(limit)\
                .execute()
            
            return result.data
            
        except Exception as e:
            print(f"Erro ao recuperar histórico: {str(e)}")
            return []
    
    def save_generated_content(self, phone_number, content_type, content, metadata=None):
        """Salva conteúdo gerado pelo assistente"""
        try:
            data = {
                'phone_number': phone_number,
                'content_type': content_type,
                'content': content,
                'metadata': metadata or {},
                'created_at': datetime.now().isoformat()
            }
            
            result = self.supabase.table('generated_content').insert(data).execute()
            return result.data
            
        except Exception as e:
            print(f"Erro ao salvar conteúdo: {str(e)}")
            return None
    
    def get_user_stats(self, phone_number):
        """Recupera estatísticas do usuário"""
        try:
            # Total de interações
            interactions = self.supabase.table('user_interactions')\
                .select('*', count='exact')\
                .eq('phone_number', phone_number)\
                .execute()
            
            # Conteúdo gerado por tipo
            content_stats = self.supabase.table('generated_content')\
                .select('content_type', count='exact')\
                .eq('phone_number', phone_number)\
                .execute()
            
            # Interações por tipo
            interaction_stats = self.supabase.table('user_interactions')\
                .select('interaction_type', count='exact')\
                .eq('phone_number', phone_number)\
                .execute()
            
            return {
                'total_interactions': interactions.count,
                'content_by_type': content_stats.data,
                'interactions_by_type': interaction_stats.data
            }
            
        except Exception as e:
            print(f"Erro ao recuperar estatísticas: {str(e)}")
            return {}
    
    def save_user_preferences(self, phone_number, preferences):
        """Salva preferências do usuário"""
        try:
            data = {
                'phone_number': phone_number,
                'preferences': preferences,
                'updated_at': datetime.now().isoformat()
            }
            
            # Upsert - insere ou atualiza
            result = self.supabase.table('user_preferences')\
                .upsert(data, on_conflict='phone_number')\
                .execute()
            
            return result.data
            
        except Exception as e:
            print(f"Erro ao salvar preferências: {str(e)}")
            return None
    
    def get_user_preferences(self, phone_number):
        """Recupera preferências do usuário"""
        try:
            result = self.supabase.table('user_preferences')\
                .select('*')\
                .eq('phone_number', phone_number)\
                .execute()
            
            if result.data:
                return result.data[0]['preferences']
            return {}
            
        except Exception as e:
            print(f"Erro ao recuperar preferências: {str(e)}")
            return {}

# Instância global do gerenciador
supabase_manager = SupabaseManager()

@supabase_bp.route('/user/<phone_number>/history', methods=['GET'])
def get_user_history(phone_number):
    """API para recuperar histórico do usuário"""
    try:
        limit = request.args.get('limit', 50, type=int)
        history = supabase_manager.get_user_history(phone_number, limit)
        
        return jsonify({
            'status': 'success',
            'data': history,
            'count': len(history)
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supabase_bp.route('/user/<phone_number>/stats', methods=['GET'])
def get_user_stats(phone_number):
    """API para recuperar estatísticas do usuário"""
    try:
        stats = supabase_manager.get_user_stats(phone_number)
        
        return jsonify({
            'status': 'success',
            'data': stats
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supabase_bp.route('/user/<phone_number>/preferences', methods=['GET', 'POST'])
def handle_user_preferences(phone_number):
    """API para gerenciar preferências do usuário"""
    try:
        if request.method == 'GET':
            preferences = supabase_manager.get_user_preferences(phone_number)
            return jsonify({
                'status': 'success',
                'data': preferences
            }), 200
        
        elif request.method == 'POST':
            preferences = request.get_json()
            result = supabase_manager.save_user_preferences(phone_number, preferences)
            
            return jsonify({
                'status': 'success',
                'data': result
            }), 200
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supabase_bp.route('/analytics/dashboard', methods=['GET'])
def get_analytics_dashboard():
    """API para dashboard de analytics"""
    try:
        # Estatísticas gerais
        total_users = supabase.table('user_interactions')\
            .select('phone_number', count='exact')\
            .execute()
        
        total_interactions = supabase.table('user_interactions')\
            .select('*', count='exact')\
            .execute()
        
        content_by_type = supabase.table('generated_content')\
            .select('content_type', count='exact')\
            .execute()
        
        # Interações por dia (últimos 30 dias)
        from datetime import datetime, timedelta
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        
        recent_interactions = supabase.table('user_interactions')\
            .select('created_at')\
            .gte('created_at', thirty_days_ago)\
            .execute()
        
        return jsonify({
            'status': 'success',
            'data': {
                'total_users': len(set([i['phone_number'] for i in total_users.data])) if total_users.data else 0,
                'total_interactions': total_interactions.count,
                'content_by_type': content_by_type.data,
                'recent_interactions_count': len(recent_interactions.data)
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@supabase_bp.route('/content/popular', methods=['GET'])
def get_popular_content():
    """API para recuperar conteúdo mais popular"""
    try:
        # Conteúdo mais gerado por tipo
        popular_content = supabase.table('generated_content')\
            .select('content_type, content')\
            .order('created_at', desc=True)\
            .limit(20)\
            .execute()
        
        return jsonify({
            'status': 'success',
            'data': popular_content.data
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Função para criar as tabelas necessárias no Supabase
def create_supabase_tables():
    """
    Execute este SQL no Supabase para criar as tabelas necessárias:
    
    -- Tabela para interações dos usuários
    CREATE TABLE user_interactions (
        id BIGSERIAL PRIMARY KEY,
        phone_number VARCHAR(20) NOT NULL,
        user_message TEXT NOT NULL,
        bot_response TEXT NOT NULL,
        interaction_type VARCHAR(50) DEFAULT 'chat',
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Tabela para conteúdo gerado
    CREATE TABLE generated_content (
        id BIGSERIAL PRIMARY KEY,
        phone_number VARCHAR(20) NOT NULL,
        content_type VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        metadata JSONB,
        created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Tabela para preferências dos usuários
    CREATE TABLE user_preferences (
        id BIGSERIAL PRIMARY KEY,
        phone_number VARCHAR(20) UNIQUE NOT NULL,
        preferences JSONB NOT NULL,
        updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
    );
    
    -- Índices para performance
    CREATE INDEX idx_user_interactions_phone ON user_interactions(phone_number);
    CREATE INDEX idx_user_interactions_created_at ON user_interactions(created_at);
    CREATE INDEX idx_generated_content_phone ON generated_content(phone_number);
    CREATE INDEX idx_generated_content_type ON generated_content(content_type);
    
    -- RLS (Row Level Security) - opcional
    ALTER TABLE user_interactions ENABLE ROW LEVEL SECURITY;
    ALTER TABLE generated_content ENABLE ROW LEVEL SECURITY;
    ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;
    """
    pass

