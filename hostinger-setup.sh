#!/bin/bash

###############################################################################
# Script de Deploy Automático - Qognix Genius Assistant
# Plataforma: Hostinger VPS
# Autor: Manus AI
# Data: 17/10/2025
###############################################################################

set -e  # Parar em caso de erro

echo "======================================================================"
echo "  Deploy Automático - Qognix Genius Assistant na Hostinger VPS"
echo "======================================================================"
echo ""

# Cores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Função para printar mensagens coloridas
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}➜ $1${NC}"
}

# Verificar se está rodando como root
if [ "$EUID" -eq 0 ]; then 
    print_error "Não execute este script como root. Use um usuário normal com sudo."
    exit 1
fi

# 1. Atualizar sistema
print_info "Atualizando sistema..."
sudo apt update && sudo apt upgrade -y
print_success "Sistema atualizado"

# 2. Instalar dependências básicas
print_info "Instalando dependências básicas..."
sudo apt install -y \
    git \
    curl \
    wget \
    build-essential \
    software-properties-common \
    ufw \
    nginx
print_success "Dependências básicas instaladas"

# 3. Instalar Python 3.11
print_info "Instalando Python 3.11..."
sudo add-apt-repository ppa:deadsnakes/ppa -y
sudo apt update
sudo apt install -y python3.11 python3.11-venv python3.11-dev python3-pip
print_success "Python 3.11 instalado"

# 4. Instalar Node.js 22 e pnpm
print_info "Instalando Node.js 22..."
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt install -y nodejs
sudo npm install -g pnpm
print_success "Node.js 22 e pnpm instalados"

# 5. Configurar firewall
print_info "Configurando firewall..."
sudo ufw allow OpenSSH
sudo ufw allow 'Nginx Full'
sudo ufw allow 5000
echo "y" | sudo ufw enable
print_success "Firewall configurado"

# 6. Clonar repositório
print_info "Clonando repositório..."
cd ~
if [ -d "qognix-genius-assistant" ]; then
    print_info "Repositório já existe. Atualizando..."
    cd qognix-genius-assistant
    git pull
else
    git clone https://github.com/pedrobatistellabit/qognix-genius-assistant.git
    cd qognix-genius-assistant
fi
print_success "Repositório clonado/atualizado"

# 7. Configurar backend
print_info "Configurando backend Python..."
cd ~/qognix-genius-assistant/backend
python3.11 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r ../requirements.txt
deactivate
print_success "Backend configurado"

# 8. Configurar frontend
print_info "Configurando e compilando frontend..."
cd ~/qognix-genius-assistant/frontend
pnpm install
pnpm run build
print_success "Frontend compilado"

# 9. Copiar build do frontend para backend
print_info "Integrando frontend com backend..."
mkdir -p ~/qognix-genius-assistant/backend/src/static
cp -r ~/qognix-genius-assistant/frontend/dist/* ~/qognix-genius-assistant/backend/src/static/
print_success "Frontend integrado"

# 10. Criar diretório para banco de dados
print_info "Criando diretório para banco de dados..."
mkdir -p ~/qognix-genius-assistant/backend/src/database
print_success "Diretório de banco de dados criado"

# 11. Criar arquivo .env
print_info "Criando arquivo de configuração..."
cat > ~/qognix-genius-assistant/backend/.env << 'EOF'
FLASK_ENV=production
PORT=5000
SECRET_KEY=change-this-to-a-random-secret-key
OPENAI_API_KEY=
WHATSAPP_TOKEN=
SUPABASE_URL=
SUPABASE_KEY=
EOF
print_success "Arquivo .env criado"

# 12. Criar serviço systemd
print_info "Criando serviço systemd..."
sudo tee /etc/systemd/system/qognix.service > /dev/null << EOF
[Unit]
Description=Qognix Genius Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/home/$USER/qognix-genius-assistant/backend
Environment="PATH=/home/$USER/qognix-genius-assistant/backend/venv/bin"
ExecStart=/home/$USER/qognix-genius-assistant/backend/venv/bin/gunicorn --bind 127.0.0.1:5000 --workers 2 --threads 4 --timeout 120 src.main:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF
print_success "Serviço systemd criado"

# 13. Configurar Nginx
print_info "Configurando Nginx..."
sudo tee /etc/nginx/sites-available/qognix > /dev/null << 'EOF'
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
EOF

# Ativar site
sudo ln -sf /etc/nginx/sites-available/qognix /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx
print_success "Nginx configurado"

# 14. Iniciar serviço
print_info "Iniciando aplicação..."
sudo systemctl daemon-reload
sudo systemctl enable qognix
sudo systemctl start qognix
print_success "Aplicação iniciada"

# 15. Verificar status
sleep 3
print_info "Verificando status..."
sudo systemctl status qognix --no-pager

echo ""
echo "======================================================================"
echo -e "${GREEN}✓ Deploy concluído com sucesso!${NC}"
echo "======================================================================"
echo ""
echo "📊 Informações do Deploy:"
echo ""
echo "  🌐 URL: http://$(curl -s ifconfig.me)"
echo "  📁 Diretório: ~/qognix-genius-assistant"
echo "  🔧 Serviço: qognix.service"
echo ""
echo "📝 Comandos Úteis:"
echo ""
echo "  Ver logs:        sudo journalctl -u qognix -f"
echo "  Reiniciar:       sudo systemctl restart qognix"
echo "  Parar:           sudo systemctl stop qognix"
echo "  Status:          sudo systemctl status qognix"
echo "  Editar .env:     nano ~/qognix-genius-assistant/backend/.env"
echo ""
echo "🔐 Próximos Passos:"
echo ""
echo "  1. Configure suas variáveis de ambiente:"
echo "     nano ~/qognix-genius-assistant/backend/.env"
echo ""
echo "  2. Reinicie o serviço após editar .env:"
echo "     sudo systemctl restart qognix"
echo ""
echo "  3. (Opcional) Configure SSL/HTTPS:"
echo "     sudo apt install certbot python3-certbot-nginx"
echo "     sudo certbot --nginx"
echo ""
echo "======================================================================"

