#!/bin/bash
# Plex Auto-Prune - One-Command Installer
# Usage: curl -sSL https://raw.githubusercontent.com/InfamousMorningstar/plex-autoprune-GUI/master/install.sh | bash

set -e

echo "🚀 Plex Auto-Prune Installer"
echo "=============================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    OS="linux"
elif [[ "$OSTYPE" == "darwin"* ]]; then
    OS="mac"
else
    echo "❌ Unsupported OS: $OSTYPE"
    exit 1
fi

# Check for Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first:"
    echo "   https://docs.docker.com/get-docker/"
    exit 1
fi

# Check for Docker Compose
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first:"
    echo "   https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker found"

# Ask for installation directory
read -p "📁 Installation directory [default: ~/plex-auto-prune]: " INSTALL_DIR
INSTALL_DIR=${INSTALL_DIR:-~/plex-auto-prune}
INSTALL_DIR=$(eval echo "$INSTALL_DIR")  # Expand ~

# Create directory
echo "📦 Creating directory: $INSTALL_DIR"
mkdir -p "$INSTALL_DIR"
cd "$INSTALL_DIR"

# Download docker-compose.yml
echo "⬇️  Downloading docker-compose.yml..."
curl -sSL https://raw.githubusercontent.com/InfamousMorningstar/plex-autoprune-GUI/master/docker-compose.yml -o docker-compose.yml

# Create directories
echo "📂 Creating state directories..."
mkdir -p state email_templates

# Ask for port
read -p "🌐 Web UI port [default: 5000]: " PORT
PORT=${PORT:-5000}

# Update port in docker-compose.yml
if [[ "$OS" == "mac" ]]; then
    sed -i '' "s/5000:5000/${PORT}:5000/g" docker-compose.yml
else
    sed -i "s/5000:5000/${PORT}:5000/g" docker-compose.yml
fi

# Pull and start container
echo "🐳 Pulling Docker image..."
docker-compose pull

echo "🚀 Starting Plex Auto-Prune..."
docker-compose up -d

# Wait for container to be healthy
echo "⏳ Waiting for application to start..."
sleep 5

# Get local IP
if [[ "$OS" == "mac" ]]; then
    LOCAL_IP=$(ipconfig getifaddr en0 || echo "localhost")
else
    LOCAL_IP=$(hostname -I | awk '{print $1}' || echo "localhost")
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎉 Plex Auto-Prune is now running!"
echo ""
echo "📍 Access the web UI at:"
echo "   Local:   http://localhost:${PORT}"
echo "   Network: http://${LOCAL_IP}:${PORT}"
echo ""
echo "🔐 Next steps:"
echo "   1. Open the web UI in your browser"
echo "   2. Login with your Plex account"
echo "   3. Complete the setup wizard (2 minutes)"
echo "   4. Start managing your users!"
echo ""
echo "📖 View logs: docker-compose logs -f"
echo "🔄 Restart:   docker-compose restart"
echo "🛑 Stop:      docker-compose down"
echo ""
