# Multi-stage build para Qognix Genius Assistant
FROM node:22-alpine AS frontend-builder

WORKDIR /app/frontend

# Copiar package files
COPY frontend/package*.json ./
COPY frontend/pnpm-lock.yaml ./

# Instalar pnpm e dependências
RUN npm install -g pnpm && \
    pnpm install --frozen-lockfile

# Copiar código fonte do frontend
COPY frontend/ ./

# Build do frontend
RUN pnpm run build

# Stage 2: Backend Python
FROM python:3.11-slim

WORKDIR /app

# Instalar dependências do sistema
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY backend/requirements.txt ./

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código do backend
COPY backend/ ./backend/

# Copiar build do frontend para static
COPY --from=frontend-builder /app/frontend/dist ./backend/static/

# Criar diretórios necessários
RUN mkdir -p /app/backend/src/database && \
    chmod -R 755 /app/backend

# Criar arquivo .env com configurações padrão
RUN echo "FLASK_ENV=production\nSECRET_KEY=change-this-in-production\nDATABASE_URL=sqlite:///./src/database/qognix.db" > /app/backend/.env

WORKDIR /app/backend

# Expor porta
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/api/health', timeout=5)" || exit 1

# Comando para iniciar (usando python direto para debug)
CMD ["python", "-m", "gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "src.main:app"]

