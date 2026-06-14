#!/bin/bash
# Envia o projeto e faz o build na VM.
# Uso: bash deploy/deploy.sh <IP_DA_VM> <CAMINHO_KEY>
# Ex:  bash deploy/deploy.sh 150.230.x.x ~/.ssh/oracle_key.pem

set -e

VM_IP="${1:?Informe o IP da VM: bash deploy.sh <IP> <KEY>}"
KEY="${2:?Informe o caminho da chave: bash deploy.sh <IP> <KEY>}"
VM_USER="opc"
APP_DIR="/opt/projeto-odds"
SSH="ssh -i $KEY -o StrictHostKeyChecking=no $VM_USER@$VM_IP"

echo "=== Enviando arquivos para $VM_IP ==="
# Exclui node_modules, __pycache__, .git, venv
rsync -avz --progress \
    --exclude='node_modules' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    --exclude='venv' \
    --exclude='frontend/dist' \
    -e "ssh -i $KEY -o StrictHostKeyChecking=no" \
    ./ "$VM_USER@$VM_IP:$APP_DIR/"

echo "=== Instalando deps Python na VM ==="
$SSH "$APP_DIR/venv/bin/pip install -q -r $APP_DIR/backend/requirements.txt"

echo "=== Build do frontend React na VM ==="
$SSH "cd $APP_DIR/frontend && npm ci --silent && npm run build"

echo "=== Reiniciando serviços ==="
$SSH "sudo systemctl restart projeto-odds-api && sudo systemctl reload nginx"

echo ""
echo "=== Deploy concluído! Acesse: http://$VM_IP ==="
