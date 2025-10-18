# Multi-stage build para Qognix Genius Assistant
FROM node:22-alpine AS frontend-builder

# Instalar pnpm
RUN npm install -g pnpm

# Copiar arquivos do frontend
WORKDIR /app/frontend
COPY frontend/package.json frontend/pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

# Copiar código fonte e fazer build
COPY frontend/ ./
RUN pnpm run build

# Stage 2: Backend Python
FROM python:3.11-slim

# Instalar dependências do sistema
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Criar diretório de trabalho
WORKDIR /app

# Copiar requirements e instalar dependências Python
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ ./backend/

# Copiar build do frontend para pasta static
COPY --from=frontend-builder /app/frontend/dist ./backend/src/static

# Criar diretório para banco de dados
RUN mkdir -p /app/backend/src/database

# Expor porta
EXPOSE 5000

# Variáveis de ambiente padrão
ENV FLASK_APP=backend/src/main.py
ENV PYTHONUNBUFFERED=1
ENV PORT=5000

# Comando de inicialização
CMD cd backend && gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 src.main:app

