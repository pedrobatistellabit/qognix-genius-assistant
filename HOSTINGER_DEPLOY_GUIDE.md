# 🚀 Guia Completo de Deploy - Hostinger VPS

## Qognix Genius Assistant na Hostinger

---

## 📋 Índice

1. [Requisitos](#requisitos)
2. [Opção 1: Deploy Automático (Recomendado)](#opção-1-deploy-automático)
3. [Opção 2: Deploy Manual](#opção-2-deploy-manual)
4. [Opção 3: Deploy com Docker](#opção-3-deploy-com-docker)
5. [Configurações Pós-Deploy](#configurações-pós-deploy)
6. [Gerenciamento e Manutenção](#gerenciamento-e-manutenção)
7. [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos

### Plano Hostinger Necessário

⚠️ **IMPORTANTE**: A hospedagem compartilhada da Hostinger **NÃO suporta Python/Flask**.

Você precisa de um **VPS Hostinger**:

- **VPS 1** (Recomendado para começar) - A partir de R$ 19,99/mês
  - 1 vCPU
  - 4 GB RAM
  - 50 GB SSD
  
- **VPS 2** (Melhor performance) - A partir de R$ 29,99/mês
  - 2 vCPU
  - 8 GB RAM
  - 100 GB SSD

### Sistema Operacional Recomendado

- **Ubuntu 22.04 LTS** (recomendado)
- **Ubuntu 20.04 LTS** (também funciona)
- **Debian 11** (alternativa)

---

## 🎯 Opção 1: Deploy Automático (Recomendado)

### ⏱️ Tempo: 10-15 minutos

Esta é a forma **mais fácil e rápida** de fazer o deploy!

### Passo 1: Acessar seu VPS

#### Via Painel Hostinger (hPanel)

1. Acesse https://hpanel.hostinger.com
2. Faça login na sua conta
3. Vá em **VPS** → Selecione seu VPS
4. Clique em **Browser Terminal** ou **SSH Access**

#### Via SSH (Recomendado)

```bash
ssh root@seu-ip-vps
# Digite a senha quando solicitado
```

**Encontrar IP do VPS**: No hPanel → VPS → Overview → IP Address

### Passo 2: Executar Script Automático

Cole estes comandos no terminal do VPS:

```bash
# 1. Baixar o script de instalação
wget https://raw.githubusercontent.com/pedrobatistellabit/qognix-genius-assistant/master/hostinger-setup.sh

# 2. Tornar executável
chmod +x hostinger-setup.sh

# 3. Executar (vai levar ~10 minutos)
./hostinger-setup.sh
```

### Passo 3: Aguardar Instalação

O script irá automaticamente:

✅ Atualizar o sistema  
✅ Instalar Python 3.11  
✅ Instalar Node.js 22  
✅ Clonar o repositório  
✅ Instalar dependências  
✅ Compilar o frontend  
✅ Configurar Nginx  
✅ Criar serviço systemd  
✅ Iniciar a aplicação  

### Passo 4: Acessar a Aplicação

Após a conclusão, acesse:

```
http://SEU-IP-VPS
```

**Pronto!** 🎉 Sua aplicação está online!

---

## 🔧 Opção 2: Deploy Manual

### ⏱️ Tempo: 30-40 minutos

Para quem prefere controle total sobre cada etapa.

### Passo 1: Conectar ao VPS

```bash
ssh root@seu-ip-vps
```

### Passo 2: Atualizar Sistema

```bash
apt update && apt upgrade -y
```

### Passo 3: Instalar Dependências

```bash
# Git e ferramentas básicas
apt install -y git curl wget build-essential software-properties-common ufw nginx

# Python 3.11
add-apt-repository ppa:deadsnakes/ppa -y
apt update
apt install -y python3.11 python3.11-venv python3.11-dev python3-pip

# Node.js 22
curl -fsSL https://deb.nodesource.com/setup_22.x | bash -
apt install -y nodejs
npm install -g pnpm
```

### Passo 4: Configurar Firewall

```bash
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw allow 5000
ufw enable
```

### Passo 5: Clonar Repositório

```bash
cd /root
git clone https://github.com/pedrobatistellabit/qognix-genius-assistant.git
cd qognix-genius-assistant
```

### Passo 6: Configurar Backend

```bash
cd /root/qognix-genius-assistant/backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt
deactivate
```

### Passo 7: Configurar Frontend

```bash
cd /root/qognix-genius-assistant/frontend
pnpm install
pnpm run build
```

### Passo 8: Integrar Frontend

```bash
mkdir -p /root/qognix-genius-assistant/backend/src/static
cp -r /root/qognix-genius-assistant/frontend/dist/* /root/qognix-genius-assistant/backend/src/static/
```

### Passo 9: Criar Arquivo .env

```bash
cd /root/qognix-genius-assistant/backend
nano .env
```

Cole este conteúdo:

```env
FLASK_ENV=production
PORT=5000
SECRET_KEY=MUDE-ISTO-PARA-UMA-CHAVE-ALEATORIA
OPENAI_API_KEY=
WHATSAPP_TOKEN=
SUPABASE_URL=
SUPABASE_KEY=
```

Salve com `Ctrl+O`, Enter, `Ctrl+X`

### Passo 10: Criar Serviço Systemd

```bash
nano /etc/systemd/system/qognix.service
```

Cole:

```ini
[Unit]
Description=Qognix Genius Assistant
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/qognix-genius-assistant/backend
Environment="PATH=/root/qognix-genius-assistant/backend/venv/bin"
ExecStart=/root/qognix-genius-assistant/backend/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 --threads 4 --timeout 120 src.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Salve e ative:

```bash
systemctl daemon-reload
systemctl enable qognix
systemctl start qognix
systemctl status qognix
```

### Passo 11: Configurar Nginx

```bash
nano /etc/nginx/sites-available/qognix
```

Cole:

```nginx
server {
    listen 80;
    server_name _;

    client_max_body_size 10M;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }
}
```

Ative e reinicie:

```bash
ln -s /etc/nginx/sites-available/qognix /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default
nginx -t
systemctl restart nginx
```

### Passo 12: Verificar

```bash
curl http://localhost
```

Acesse: `http://SEU-IP-VPS`

---

## 🐳 Opção 3: Deploy com Docker

### ⏱️ Tempo: 15-20 minutos

### Passo 1: Conectar ao VPS

```bash
ssh root@seu-ip-vps
```

### Passo 2: Instalar Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Passo 3: Clonar e Executar

```bash
cd /root
git clone https://github.com/pedrobatistellabit/qognix-genius-assistant.git
cd qognix-genius-assistant
docker-compose up -d
```

### Passo 4: Configurar Firewall

```bash
apt install -y ufw
ufw allow OpenSSH
ufw allow 5000
ufw enable
```

### Passo 5: Acessar

```
http://SEU-IP-VPS:5000
```

---

## ⚙️ Configurações Pós-Deploy

### 1. Configurar Variáveis de Ambiente

```bash
nano /root/qognix-genius-assistant/backend/.env
```

Adicione suas chaves de API:

```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxx
WHATSAPP_TOKEN=EAAxxxxxxxxxxxxxxxxx
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Reinicie:

```bash
systemctl restart qognix
```

### 2. Configurar Domínio (Opcional)

#### No Painel da Hostinger:

1. Vá em **Domínios**
2. Clique em **Gerenciar DNS**
3. Adicione um registro A:
   - **Tipo**: A
   - **Nome**: @ (ou subdomínio desejado)
   - **Aponta para**: IP do seu VPS
   - **TTL**: 14400

#### No VPS:

Edite a configuração do Nginx:

```bash
nano /etc/nginx/sites-available/qognix
```

Altere a linha `server_name`:

```nginx
server_name seu-dominio.com www.seu-dominio.com;
```

Reinicie:

```bash
nginx -t
systemctl restart nginx
```

### 3. Configurar SSL/HTTPS (Recomendado)

```bash
# Instalar Certbot
apt install -y certbot python3-certbot-nginx

# Obter certificado SSL
certbot --nginx -d seu-dominio.com -d www.seu-dominio.com

# Renovação automática já está configurada!
```

Acesse: `https://seu-dominio.com`

---

## 🛠️ Gerenciamento e Manutenção

### Comandos Úteis

```bash
# Ver logs em tempo real
journalctl -u qognix -f

# Reiniciar aplicação
systemctl restart qognix

# Parar aplicação
systemctl stop qognix

# Iniciar aplicação
systemctl start qognix

# Ver status
systemctl status qognix

# Reiniciar Nginx
systemctl restart nginx
```

### Atualizar Aplicação

```bash
cd /root/qognix-genius-assistant
git pull
cd frontend
pnpm install
pnpm run build
cp -r dist/* ../backend/src/static/
systemctl restart qognix
```

### Backup do Banco de Dados

```bash
# Criar backup
cp /root/qognix-genius-assistant/backend/src/database/app.db \
   /root/backup-$(date +%Y%m%d).db

# Restaurar backup
cp /root/backup-20251017.db \
   /root/qognix-genius-assistant/backend/src/database/app.db
systemctl restart qognix
```

### Monitoramento

```bash
# Ver uso de recursos
htop

# Ver uso de disco
df -h

# Ver uso de memória
free -h

# Ver processos Python
ps aux | grep python
```

---

## 🔍 Troubleshooting

### Problema: Aplicação não inicia

```bash
# Verificar logs
journalctl -u qognix -n 50

# Verificar se a porta está em uso
netstat -tuln | grep 5000

# Reiniciar serviço
systemctl restart qognix
```

### Problema: Erro 502 Bad Gateway

```bash
# Verificar se o backend está rodando
systemctl status qognix

# Verificar logs do Nginx
tail -f /var/log/nginx/error.log

# Reiniciar ambos
systemctl restart qognix
systemctl restart nginx
```

### Problema: Permissões negadas

```bash
# Corrigir permissões
chown -R root:root /root/qognix-genius-assistant
chmod -R 755 /root/qognix-genius-assistant
```

### Problema: Falta de memória

```bash
# Criar swap (2GB)
fallocate -l 2G /swapfile
chmod 600 /swapfile
mkswap /swapfile
swapon /swapfile
echo '/swapfile none swap sw 0 0' >> /etc/fstab
```

### Problema: Frontend não carrega

```bash
# Verificar se os arquivos estão no lugar certo
ls -la /root/qognix-genius-assistant/backend/src/static/

# Recompilar frontend
cd /root/qognix-genius-assistant/frontend
pnpm run build
cp -r dist/* ../backend/src/static/
systemctl restart qognix
```

---

## 📊 Informações Adicionais

### Portas Utilizadas

- **5000**: Aplicação Flask (interno)
- **80**: HTTP (Nginx)
- **443**: HTTPS (Nginx, após SSL)

### Arquivos Importantes

- **Aplicação**: `/root/qognix-genius-assistant/`
- **Configuração**: `/root/qognix-genius-assistant/backend/.env`
- **Banco de Dados**: `/root/qognix-genius-assistant/backend/src/database/app.db`
- **Logs**: `journalctl -u qognix`
- **Nginx Config**: `/etc/nginx/sites-available/qognix`
- **Serviço**: `/etc/systemd/system/qognix.service`

### Recursos do VPS

Monitore o uso de recursos no hPanel:
- CPU
- RAM
- Disco
- Tráfego

---

## 🆘 Suporte

### Documentação

- **Repositório GitHub**: https://github.com/pedrobatistellabit/qognix-genius-assistant
- **Guia Geral de Deploy**: DEPLOY_GUIDE.md

### Suporte Hostinger

- **hPanel**: https://hpanel.hostinger.com
- **Chat**: Disponível 24/7 no hPanel
- **Base de Conhecimento**: https://support.hostinger.com

### Comunidade

- **Issues GitHub**: https://github.com/pedrobatistellabit/qognix-genius-assistant/issues

---

## ✅ Checklist de Deploy

- [ ] VPS Hostinger contratado
- [ ] Sistema operacional Ubuntu 22.04 instalado
- [ ] Acesso SSH configurado
- [ ] Script de deploy executado
- [ ] Aplicação acessível via IP
- [ ] Variáveis de ambiente configuradas
- [ ] Domínio apontado (opcional)
- [ ] SSL/HTTPS configurado (opcional)
- [ ] Backup configurado
- [ ] Monitoramento ativo

---

## 🎉 Conclusão

Parabéns! Seu **Qognix Genius Assistant** está agora rodando permanentemente no VPS Hostinger!

A aplicação está configurada para:
- ✅ Reiniciar automaticamente em caso de falha
- ✅ Iniciar automaticamente após reboot do servidor
- ✅ Servir requisições através do Nginx
- ✅ Escalar conforme necessário

**Boa sorte com seu projeto! 🚀**

---

**Criado em**: 17 de Outubro de 2025  
**Plataforma**: Hostinger VPS  
**Versão**: 1.0

