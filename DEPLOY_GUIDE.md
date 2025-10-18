# 🚀 Guia Completo de Deploy - Qognix Genius Assistant

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Deploy com Docker (Recomendado)](#deploy-com-docker)
3. [Deploy em Plataformas Cloud](#deploy-em-plataformas-cloud)
4. [Deploy Manual](#deploy-manual)
5. [Configurações de Produção](#configurações-de-produção)
6. [Troubleshooting](#troubleshooting)

---

## 🎯 Visão Geral

O Qognix Genius Assistant é uma aplicação full-stack composta por:

- **Frontend**: React 19 + Vite + Tailwind CSS
- **Backend**: Flask (Python 3.11)
- **Banco de Dados**: SQLite (local) ou Supabase (cloud)
- **APIs**: OpenAI GPT-4, WhatsApp Business

### Requisitos Mínimos

- **CPU**: 1 core
- **RAM**: 512 MB
- **Disco**: 1 GB
- **Porta**: 5000 (configurável)

---

## 🐳 Deploy com Docker (Recomendado)

### Opção 1: Docker Compose (Mais Fácil)

```bash
# 1. Clone o repositório
git clone https://github.com/pedrobatistellabit/qognix-genius-assistant.git
cd qognix-genius-assistant

# 2. Configure variáveis de ambiente (opcional)
cp .env.example .env
# Edite o arquivo .env com suas credenciais

# 3. Inicie a aplicação
docker-compose up -d

# 4. Verifique os logs
docker-compose logs -f

# 5. Acesse a aplicação
# http://localhost:5000
```

### Opção 2: Docker Build Manual

```bash
# 1. Build da imagem
docker build -t qognix-genius-assistant .

# 2. Execute o container
docker run -d \
  --name qognix-app \
  -p 5000:5000 \
  -v $(pwd)/backend/src/database:/app/backend/src/database \
  -e PORT=5000 \
  qognix-genius-assistant

# 3. Verifique o status
docker ps
docker logs qognix-app
```

### Comandos Úteis Docker

```bash
# Parar a aplicação
docker-compose down

# Reiniciar
docker-compose restart

# Ver logs em tempo real
docker-compose logs -f qognix-app

# Remover tudo e reconstruir
docker-compose down -v
docker-compose up -d --build
```

---

## ☁️ Deploy em Plataformas Cloud

### 1. Render.com

**Passos:**

1. Acesse [render.com](https://render.com) e faça login com GitHub
2. Clique em **New** → **Web Service**
3. Conecte o repositório `qognix-genius-assistant`
4. Configure:
   - **Name**: qognix-genius-assistant
   - **Region**: Oregon (US West)
   - **Branch**: main
   - **Build Command**: 
     ```bash
     pip install -r requirements.txt && cd frontend && pnpm install && pnpm run build && cp -r dist/* ../backend/src/static/
     ```
   - **Start Command**: 
     ```bash
     cd backend && gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 src.main:app
     ```
   - **Instance Type**: Free
5. Adicione variáveis de ambiente (opcional):
   - `OPENAI_API_KEY`
   - `WHATSAPP_TOKEN`
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
6. Clique em **Create Web Service**

**URL Final**: `https://qognix-genius-assistant.onrender.com`

---

### 2. Railway.app

**Passos:**

1. Acesse [railway.app](https://railway.app) e faça login com GitHub
2. Clique em **New Project** → **Deploy from GitHub repo**
3. Selecione `qognix-genius-assistant`
4. Railway detectará automaticamente o `Dockerfile`
5. Configure variáveis de ambiente (Settings → Variables):
   - `PORT=5000`
   - `OPENAI_API_KEY` (opcional)
   - `WHATSAPP_TOKEN` (opcional)
6. Aguarde o deploy automático

**URL Final**: Gerada automaticamente pelo Railway

---

### 3. Heroku

**Passos:**

```bash
# 1. Instale Heroku CLI
# https://devcenter.heroku.com/articles/heroku-cli

# 2. Login no Heroku
heroku login

# 3. Crie a aplicação
heroku create qognix-genius-assistant

# 4. Configure buildpacks
heroku buildpacks:add --index 1 heroku/nodejs
heroku buildpacks:add --index 2 heroku/python

# 5. Configure variáveis de ambiente
heroku config:set FLASK_ENV=production
heroku config:set OPENAI_API_KEY=sua_chave_aqui

# 6. Deploy
git push heroku main

# 7. Abra a aplicação
heroku open
```

**URL Final**: `https://qognix-genius-assistant.herokuapp.com`

---

### 4. DigitalOcean App Platform

**Passos:**

1. Acesse [DigitalOcean](https://cloud.digitalocean.com/apps)
2. Clique em **Create App**
3. Conecte o repositório GitHub
4. Configure:
   - **Resource Type**: Web Service
   - **Dockerfile Path**: `/Dockerfile`
   - **HTTP Port**: 5000
5. Escolha o plano (Basic - $5/mês ou Free Trial)
6. Adicione variáveis de ambiente
7. Clique em **Create Resources**

---

### 5. AWS (EC2 + Docker)

**Passos:**

```bash
# 1. Conecte-se à instância EC2
ssh -i sua-chave.pem ubuntu@seu-ip-ec2

# 2. Instale Docker
sudo apt update
sudo apt install -y docker.io docker-compose
sudo usermod -aG docker $USER

# 3. Clone o repositório
git clone https://github.com/pedrobatistellabit/qognix-genius-assistant.git
cd qognix-genius-assistant

# 4. Inicie com Docker Compose
docker-compose up -d

# 5. Configure firewall (Security Group)
# Libere a porta 5000 no AWS Console
```

**URL Final**: `http://seu-ip-ec2:5000`

---

## 🔧 Deploy Manual (Sem Docker)

### Requisitos

- Python 3.11+
- Node.js 22+
- pnpm

### Passos

```bash
# 1. Clone o repositório
git clone https://github.com/pedrobatistellabit/qognix-genius-assistant.git
cd qognix-genius-assistant

# 2. Configure o backend
cd backend
python3.11 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r ../requirements.txt

# 3. Configure o frontend
cd ../frontend
pnpm install
pnpm run build

# 4. Copie o build para o backend
cp -r dist/* ../backend/src/static/

# 5. Configure variáveis de ambiente
cd ../backend
cp .env.example .env
# Edite o arquivo .env

# 6. Inicie o servidor
gunicorn --bind 0.0.0.0:5000 --workers 2 --threads 4 src.main:app
```

### Manter Rodando em Background (Linux)

```bash
# Usando nohup
nohup gunicorn --bind 0.0.0.0:5000 --workers 2 src.main:app > app.log 2>&1 &

# Usando systemd (recomendado)
sudo nano /etc/systemd/system/qognix.service
```

Conteúdo do arquivo `qognix.service`:

```ini
[Unit]
Description=Qognix Genius Assistant
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/qognix-genius-assistant/backend
Environment="PATH=/home/ubuntu/qognix-genius-assistant/backend/venv/bin"
ExecStart=/home/ubuntu/qognix-genius-assistant/backend/venv/bin/gunicorn --bind 0.0.0.0:5000 --workers 2 src.main:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Ative o serviço:

```bash
sudo systemctl daemon-reload
sudo systemctl enable qognix
sudo systemctl start qognix
sudo systemctl status qognix
```

---

## ⚙️ Configurações de Produção

### Variáveis de Ambiente

Crie um arquivo `.env` na raiz do projeto:

```env
# Flask
FLASK_ENV=production
PORT=5000

# OpenAI (Opcional - para funcionalidades de IA)
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx

# WhatsApp Business (Opcional)
WHATSAPP_TOKEN=EAAxxxxxxxxxxxxxxxxx
WHATSAPP_PHONE_NUMBER_ID=123456789

# Supabase (Opcional - para banco de dados em nuvem)
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

# Segurança
SECRET_KEY=sua-chave-secreta-aqui-gere-uma-aleatoria
```

### Gerar SECRET_KEY

```python
import secrets
print(secrets.token_hex(32))
```

### Nginx Reverse Proxy (Recomendado)

```nginx
server {
    listen 80;
    server_name seu-dominio.com;

    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### SSL/HTTPS com Certbot

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d seu-dominio.com
```

---

## 🔍 Troubleshooting

### Erro: "Port 5000 already in use"

```bash
# Encontre o processo usando a porta
sudo lsof -i :5000

# Mate o processo
sudo kill -9 <PID>

# Ou use outra porta
PORT=8000 docker-compose up -d
```

### Erro: "Module not found"

```bash
# Reinstale as dependências
pip install -r requirements.txt --force-reinstall
```

### Frontend não carrega

```bash
# Verifique se o build foi copiado corretamente
ls -la backend/src/static/

# Reconstrua o frontend
cd frontend
pnpm run build
cp -r dist/* ../backend/src/static/
```

### Banco de dados não inicializa

```bash
# Crie o diretório manualmente
mkdir -p backend/src/database

# Verifique permissões
chmod 755 backend/src/database
```

### Logs não aparecem

```bash
# Docker
docker-compose logs -f

# Systemd
sudo journalctl -u qognix -f

# Manual
tail -f app.log
```

---

## 📊 Monitoramento

### Healthcheck

```bash
curl http://localhost:5000/
```

### Métricas

```bash
# Ver uso de recursos do Docker
docker stats qognix-app

# Ver processos
ps aux | grep gunicorn
```

---

## 🔒 Segurança

### Checklist de Produção

- [ ] Configurar HTTPS/SSL
- [ ] Usar variáveis de ambiente para segredos
- [ ] Configurar firewall (UFW ou Security Groups)
- [ ] Limitar acesso ao banco de dados
- [ ] Configurar CORS adequadamente
- [ ] Implementar rate limiting
- [ ] Fazer backup regular do banco de dados
- [ ] Monitorar logs de erro

---

## 📞 Suporte

- **Repositório**: https://github.com/pedrobatistellabit/qognix-genius-assistant
- **Issues**: https://github.com/pedrobatistellabit/qognix-genius-assistant/issues
- **Documentação**: README.md

---

**Última atualização**: 17 de Outubro de 2025

