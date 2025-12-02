#!/bin/bash

echo "🚀 Configurando AR.js para iPhone con HTTPS"
echo "=========================================="
echo ""

# Verificar si el servidor está corriendo
if ! lsof -i :5173 > /dev/null 2>&1; then
    echo "⚠️  El servidor de Vite no está corriendo"
    echo "   Por favor, ejecuta en otra terminal:"
    echo "   npm run dev"
    echo ""
    exit 1
fi

echo "✅ Servidor Vite detectado en puerto 5173"
echo ""

# Verificar si ngrok está instalado
if ! command -v ngrok &> /dev/null; then
    echo "📦 ngrok no está instalado. Instalando..."
    echo ""
    echo "Descargando ngrok..."
    
    # Detectar arquitectura
    ARCH=$(uname -m)
    if [ "$ARCH" = "arm64" ]; then
        URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-arm64.zip"
    else
        URL="https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-darwin-amd64.zip"
    fi
    
    # Descargar y descomprimir
    curl -Lo ngrok.zip "$URL"
    unzip ngrok.zip
    chmod +x ngrok
    
    # Mover a /usr/local/bin
    if [ -w /usr/local/bin ]; then
        mv ngrok /usr/local/bin/
    else
        sudo mv ngrok /usr/local/bin/
    fi
    
    rm ngrok.zip
    
    echo "✅ ngrok instalado correctamente"
    echo ""
fi

echo "🌐 Iniciando túnel HTTPS con ngrok..."
echo ""
echo "╔════════════════════════════════════════════════════╗"
echo "║  IMPORTANTE: COPIA LA URL HTTPS QUE APARECERÁ     ║"
echo "║  Y ÁBRELA EN SAFARI DE TU IPHONE                  ║"
echo "╚════════════════════════════════════════════════════╝"
echo ""
echo "Presiona CTRL+C para detener el túnel"
echo ""

# Iniciar ngrok
ngrok http 5173
