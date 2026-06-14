#!/bin/bash
# Roda UMA VEZ na VM para instalar dependências e configurar tudo.
# Execute como: bash setup-vm.sh
set -e

APP_DIR="/opt/projeto-odds"

echo "=== [1/6] Atualizando pacotes ==="
sudo dnf update -y 2>/dev/null || sudo apt-get update -y

echo "=== [2/6] Instalando Python 3.11, pip, Node 20, Nginx ==="
# Oracle Linux / RHEL
if command -v dnf &>/dev/null; then
    sudo dnf install -y python3.11 python3.11-pip nodejs nginx git
    # Node 20 via nodesource se não vier 20+
    node --version | grep -qE 'v(20|21|22)' || (
        curl -fsSL https://rpm.nodesource.com/setup_20.x | sudo bash -
        sudo dnf install -y nodejs
    )
# Ubuntu / Debian
else
    sudo apt-get install -y python3.11 python3.11-venv python3-pip nginx git curl
    node --version | grep -qE 'v(20|21|22)' || (
        curl -fsSL https://deb.nodesource.com/setup_20.x | sudo bash -
        sudo apt-get install -y nodejs
    )
fi

echo "=== [3/6] Criando diretório da aplicação ==="
sudo mkdir -p "$APP_DIR"
sudo chown opc:opc "$APP_DIR"

echo "=== [4/6] Criando virtualenv Python e instalando dependências ==="
python3.11 -m venv "$APP_DIR/venv"
"$APP_DIR/venv/bin/pip" install --upgrade pip
"$APP_DIR/venv/bin/pip" install -r "$APP_DIR/backend/requirements.txt"

echo "=== [5/6] Configurando systemd service ==="
sudo cp "$APP_DIR/deploy/projeto-odds-api.service" /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable projeto-odds-api
sudo systemctl start projeto-odds-api

echo "=== [6/6] Configurando Nginx ==="
sudo cp "$APP_DIR/deploy/nginx.conf" /etc/nginx/conf.d/projeto-odds.conf
# Remove config padrão se existir
sudo rm -f /etc/nginx/sites-enabled/default 2>/dev/null || true
sudo sed -i 's|include /etc/nginx/sites-enabled/\*|# include /etc/nginx/sites-enabled/*|' /etc/nginx/nginx.conf 2>/dev/null || true
sudo nginx -t
sudo systemctl enable nginx
sudo systemctl restart nginx

# Abre firewall interno (Oracle Linux usa firewalld)
if command -v firewall-cmd &>/dev/null; then
    sudo firewall-cmd --permanent --add-service=http
    sudo firewall-cmd --permanent --add-service=https
    sudo firewall-cmd --reload
fi

echo ""
echo "=== Setup concluído! ==="
echo "Backend:  sudo systemctl status projeto-odds-api"
echo "Logs API: sudo journalctl -u projeto-odds-api -f"
echo "Nginx:    sudo systemctl status nginx"
