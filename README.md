# Qognix Genius - Assistente de IA Criativo

Um assistente de IA avançado que vai além da automação básica, oferecendo funcionalidades criativas, análises proativas e integração completa com WhatsApp.

## 🚀 Funcionalidades Principais

### 🎨 Geração de Conteúdo Criativo
- **Posts para Redes Sociais**: Criação automática de posts para Instagram, Facebook e WhatsApp
- **Textos Persuasivos**: Geração de conteúdo com diferentes tons de voz
- **Ideias Criativas**: Brainstorming e geração de conceitos inovadores
- **Hashtags Inteligentes**: Sugestões de hashtags relevantes e engajadoras

### 📊 Análise e Sugestões Proativas
- **Otimização de Agenda**: Análise de produtividade e sugestões de melhorias
- **Conselheiro Financeiro**: Análise de gastos e sugestões de economia
- **Insights Personalizados**: Relatórios e análises baseados no comportamento do usuário
- **Daily Digest**: Resumos diários personalizados

### 🤖 Automação Inteligente
- **Múltiplas Tarefas Simultâneas**: Execução eficiente de várias operações
- **Lembretes Proativos**: Sistema inteligente de notificações
- **Integração WhatsApp**: Comunicação direta via WhatsApp Business API
- **Personalização Adaptativa**: Aprendizado contínuo das preferências do usuário

## 🏗️ Arquitetura do Sistema

### Frontend (React + TypeScript)
- Interface moderna e responsiva
- Componentes reutilizáveis com shadcn/ui
- Integração com APIs do backend
- Dashboard de analytics em tempo real

### Backend (Flask + Python)
- API RESTful robusta
- Integração com OpenAI GPT-4
- Webhook para WhatsApp Business API
- Sistema de autenticação e autorização

### Banco de Dados (Supabase)
- PostgreSQL com funcionalidades em tempo real
- Armazenamento de interações e preferências
- Analytics e métricas de uso
- Backup automático e escalabilidade

## 📁 Estrutura do Projeto

```
qognix-genius-complete/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   ├── hooks/          # Custom hooks
│   │   ├── lib/            # Utilitários
│   │   └── assets/         # Recursos estáticos
│   ├── package.json
│   └── vite.config.js
├── backend/                 # API Flask
│   ├── src/
│   │   ├── routes/         # Rotas da API
│   │   │   ├── whatsapp.py        # Integração WhatsApp
│   │   │   ├── supabase_integration.py  # Integração Supabase
│   │   │   └── user.py            # Rotas de usuário
│   │   ├── models/         # Modelos de dados
│   │   └── main.py         # Ponto de entrada
│   ├── requirements.txt
│   └── venv/
└── README.md
```

## 🛠️ Configuração e Instalação

### Pré-requisitos
- Node.js 18+
- Python 3.9+
- Conta no Supabase
- Conta no OpenAI
- WhatsApp Business API (opcional)

### 1. Configuração do Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

pip install -r requirements.txt
```

### 2. Variáveis de Ambiente

Crie um arquivo `.env` no diretório `backend/`:

```env
# OpenAI
OPENAI_API_KEY=sua_chave_openai_aqui

# Supabase
SUPABASE_URL=https://seu-projeto.supabase.co
SUPABASE_ANON_KEY=sua_chave_supabase_aqui

# WhatsApp (opcional)
WHATSAPP_TOKEN=seu_token_whatsapp
WHATSAPP_VERIFY_TOKEN=qognix_genius_webhook_token

# Flask
FLASK_ENV=development
SECRET_KEY=sua_chave_secreta_aqui
```

### 3. Configuração do Supabase

Execute o seguinte SQL no seu projeto Supabase:

```sql
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
```

### 4. Configuração do Frontend

```bash
cd frontend
pnpm install
pnpm run dev
```

### 5. Executar o Backend

```bash
cd backend
source venv/bin/activate
python src/main.py
```

## 📱 Integração com WhatsApp

### Configuração do Webhook

1. Configure o webhook no WhatsApp Business API:
   - URL: `https://seu-dominio.com/api/whatsapp/webhook`
   - Verify Token: `qognix_genius_webhook_token`

2. O sistema processará automaticamente:
   - Mensagens recebidas
   - Geração de respostas criativas
   - Salvamento no Supabase
   - Análise de sentimento e contexto

### Funcionalidades via WhatsApp

- **Criação de Posts**: "Crie um post para Instagram sobre produtividade"
- **Análise Financeira**: "Analise meus gastos e dê sugestões"
- **Otimização de Agenda**: "Como posso melhorar minha agenda?"
- **Ideias Criativas**: "Preciso de ideias para minha campanha"

## 🔧 APIs Disponíveis

### WhatsApp
- `POST /api/whatsapp/webhook` - Webhook para mensagens
- `POST /api/whatsapp/send-message` - Enviar mensagem
- `POST /api/whatsapp/generate-content` - Gerar conteúdo

### Supabase
- `GET /api/supabase/user/{phone}/history` - Histórico do usuário
- `GET /api/supabase/user/{phone}/stats` - Estatísticas do usuário
- `GET/POST /api/supabase/user/{phone}/preferences` - Preferências
- `GET /api/supabase/analytics/dashboard` - Dashboard analytics

## 📊 Monitoramento e Analytics

O sistema inclui:
- Dashboard em tempo real
- Métricas de uso e engajamento
- Análise de conteúdo gerado
- Estatísticas por usuário
- Relatórios de performance

## 🚀 Deploy

### Backend (Flask)
```bash
# Instalar dependências
pip install -r requirements.txt

# Executar em produção
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

### Frontend (React)
```bash
# Build para produção
pnpm run build

# Servir arquivos estáticos
# Os arquivos serão servidos pelo Flask
```

## 🤝 Contribuição

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 📞 Suporte

Para suporte e dúvidas:
- Email: suporte@qognix.com
- WhatsApp: +55 11 99999-9999
- Discord: [Servidor da Comunidade]

## 🎯 Roadmap

### Próximas Funcionalidades
- [ ] Integração com Instagram Direct
- [ ] Geração de imagens com DALL-E
- [ ] Análise de sentimento avançada
- [ ] Integração com Google Calendar
- [ ] Sistema de templates personalizados
- [ ] API para integrações externas
- [ ] Dashboard mobile
- [ ] Suporte a múltiplos idiomas

---

**Desenvolvido com ❤️ pela equipe Qognix**

