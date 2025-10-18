# Qognix Genius Assistant - Informações de Deploy

## ✅ Status do Deploy

**Status:** ✅ **ONLINE E FUNCIONANDO**  
**Data do Deploy:** 17 de outubro de 2025  
**Ambiente:** Sandbox Manus (Nuvem)

---

## 🌐 Acesso à Aplicação

### URL Pública
**https://5000-ifs8dora33irtrx34zpv9-bfe3eb48.manusvm.computer**

A aplicação está acessível publicamente através desta URL. O frontend React está integrado ao backend Flask e sendo servido através da mesma porta.

---

## 🏗️ Arquitetura Implementada

### Backend (Flask + Python)
- **Framework:** Flask 3.1.1
- **Porta:** 5000
- **Host:** 0.0.0.0 (todas as interfaces)
- **Banco de Dados:** SQLite local (app.db)
- **CORS:** Habilitado para todas as origens

### Frontend (React + Vite)
- **Framework:** React 19.1.0
- **Build Tool:** Vite 6.3.5
- **UI Library:** Radix UI + Tailwind CSS 4.1.7
- **Build:** Compilado e servido pelo Flask

### Estrutura de Diretórios
```
/home/ubuntu/qognix-genius-assistant/
├── backend/
│   ├── src/
│   │   ├── main.py              # Servidor Flask principal
│   │   ├── static/              # Frontend compilado
│   │   │   ├── index.html
│   │   │   └── assets/
│   │   ├── database/            # SQLite database
│   │   ├── models/              # Modelos de dados
│   │   └── routes/              # Rotas da API
│   │       ├── user.py
│   │       ├── whatsapp.py
│   │       └── supabase_integration.py
│   └── requirements.txt
└── frontend/
    ├── dist/                    # Build de produção
    ├── src/
    └── package.json
```

---

## 🔌 APIs Disponíveis

### Rotas de Usuário
- **Base URL:** `/api/`
- Gerenciamento de usuários e autenticação

### Rotas WhatsApp
- **Base URL:** `/api/whatsapp/`
- `POST /webhook` - Webhook para mensagens
- `POST /send-message` - Enviar mensagem
- `POST /generate-content` - Gerar conteúdo

### Rotas Supabase (Opcional)
- **Base URL:** `/api/supabase/`
- `GET /user/<phone>/history` - Histórico do usuário
- `GET /user/<phone>/stats` - Estatísticas
- `GET/POST /user/<phone>/preferences` - Preferências
- `GET /analytics/dashboard` - Dashboard analytics

**Nota:** As rotas Supabase estão configuradas mas não requerem conexão ativa. O sistema funciona com SQLite local.

---

## ⚙️ Configurações

### Variáveis de Ambiente
Arquivo: `/home/ubuntu/qognix-genius-assistant/backend/.env`

```env
# OpenAI Configuration
OPENAI_API_KEY=${OPENAI_API_KEY}

# Supabase Configuration (opcional)
SUPABASE_URL=https://demo.supabase.co
SUPABASE_ANON_KEY=demo-key

# WhatsApp Business API (Optional)
WHATSAPP_TOKEN=demo-token
WHATSAPP_VERIFY_TOKEN=qognix_genius_webhook_token
WHATSAPP_PHONE_NUMBER_ID=demo-phone-id

# Flask Configuration
FLASK_ENV=development
SECRET_KEY=qognix-genius-secret-key-2025
DEBUG=False

# Database
DATABASE_URL=sqlite:///app.db

# CORS Settings
CORS_ORIGINS=*
```

### Dependências Instaladas

**Backend (Python):**
- Flask 3.1.1
- flask-cors 6.0.0
- Flask-SQLAlchemy 3.1.1
- openai 1.3.0
- supabase 2.0.0
- python-dotenv 1.0.0
- requests 2.31.0

**Frontend (Node.js):**
- React 19.1.0
- Vite 6.3.5
- Tailwind CSS 4.1.7
- Radix UI (componentes completos)
- React Router DOM 7.6.1
- Recharts 2.15.3
- Framer Motion 12.15.0

---

## 🚀 Processo de Deploy Realizado

### 1. Clonagem do Repositório
```bash
gh repo clone pedrobatistellabit/qognix-genius-assistant
```

### 2. Instalação de Dependências Backend
```bash
cd backend
pip3 install -r requirements.txt
```

### 3. Instalação de Dependências Frontend
```bash
cd frontend
pnpm install
pnpm approve-builds  # Aprovação de @tailwindcss/oxide e esbuild
```

### 4. Build do Frontend
```bash
pnpm run build
# Output: dist/ com 251KB de JavaScript e 87KB de CSS
```

### 5. Integração Frontend + Backend
```bash
cp -r frontend/dist/* backend/src/static/
```

### 6. Configuração de Ambiente
- Criação do arquivo `.env` com configurações
- Criação do diretório `database/` para SQLite
- Modificação do código para tornar Supabase opcional

### 7. Inicialização do Servidor
```bash
cd backend
python3.11 src/main.py
```

### 8. Exposição Pública
```bash
# Porta 5000 exposta via proxy público
```

---

## 📊 Funcionalidades Implementadas

### ✅ Operacionais
- ✅ Servidor Flask rodando na porta 5000
- ✅ Frontend React compilado e servido
- ✅ CORS habilitado para acesso externo
- ✅ Banco de dados SQLite inicializado
- ✅ Rotas de API configuradas
- ✅ Sistema de arquivos estáticos funcionando
- ✅ Acesso público via URL

### ⚠️ Requerem Configuração Externa
- ⚠️ Integração OpenAI (requer chave de API válida)
- ⚠️ Integração WhatsApp Business (requer token e configuração)
- ⚠️ Integração Supabase (opcional, sistema funciona sem)

---

## 🔍 Verificação de Status

### Verificar se o servidor está rodando
```bash
ps aux | grep "python3.11 src/main.py"
```

### Verificar logs
```bash
cat /tmp/qognix.log
```

### Testar localmente
```bash
curl -I http://localhost:5000/
```

### Testar publicamente
```bash
curl -I https://5000-ifs8dora33irtrx34zpv9-bfe3eb48.manusvm.computer
```

---

## 📝 Observações Importantes

### Localização
O programa está instalado no **sandbox Manus**, um ambiente isolado na nuvem. Isso significa:
- ✅ Acesso via internet através de URL pública
- ✅ Ambiente Linux Ubuntu 22.04
- ✅ Recursos computacionais dedicados
- ✅ Isolamento e segurança
- ⚠️ Temporário - dados podem ser perdidos após inatividade prolongada

### Persistência
- O servidor está rodando em **modo background** (nohup)
- O processo continuará ativo enquanto o sandbox estiver ativo
- Para deploy permanente, considere plataformas como:
  - Heroku
  - Railway
  - Render
  - DigitalOcean
  - AWS/GCP/Azure

### Segurança
- A aplicação está configurada para desenvolvimento
- Para produção, considere:
  - Usar servidor WSGI (Gunicorn/uWSGI)
  - Configurar HTTPS com certificado SSL
  - Restringir CORS para domínios específicos
  - Implementar rate limiting
  - Adicionar autenticação robusta

---

## 🎯 Próximos Passos Sugeridos

1. **Testar a Interface:** Acesse a URL pública e explore a interface
2. **Configurar OpenAI:** Adicione uma chave de API válida para funcionalidades de IA
3. **Personalizar:** Ajuste cores, textos e funcionalidades conforme necessário
4. **Deploy Permanente:** Migre para plataforma de hosting permanente
5. **Monitoramento:** Configure logs e métricas para produção

---

**Deploy realizado com sucesso! 🎉**

*Documento gerado automaticamente em 17/10/2025*

