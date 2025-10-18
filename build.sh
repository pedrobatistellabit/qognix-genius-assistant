#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing frontend dependencies..."
cd frontend
pnpm install
pnpm approve-builds || true

echo "Building frontend..."
pnpm run build

echo "Copying frontend build to backend static folder..."
mkdir -p ../backend/src/static
cp -r dist/* ../backend/src/static/

echo "Build completed successfully!"

