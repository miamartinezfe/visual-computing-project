#!/bin/bash

# Script para descargar modelos 3D gratuitos
# Modelos de Poly Pizza y Quaternius (CC0 License)

cd "$(dirname "$0")/public/models"

echo "📦 Descargando modelos 3D gratuitos..."

# Robot de Poly Pizza (low poly)
echo "⬇️  Descargando Robot..."
curl -L -o robot.glb "https://models.readyplayer.me/6563c8f9b4d89d3a21e26bdd.glb"

# Árbol low poly
echo "⬇️  Descargando Tree..."
curl -L -o tree.glb "https://vazxmixjsiawhamofees.supabase.co/storage/v1/object/public/models/tree-lime/model.gltf"

# Spaceship
echo "⬇️  Descargando Spaceship..."
curl -L -o spaceship.glb "https://vazxmixjsiawhamofees.supabase.co/storage/v1/object/public/models/spaceship/model.gltf"

echo "✅ Modelos descargados en public/models/"
echo ""
echo "Modelos disponibles:"
echo "  - robot.glb (personaje low-poly)"
echo "  - tree.glb (árbol estilizado)"
echo "  - spaceship.glb (nave espacial)"
