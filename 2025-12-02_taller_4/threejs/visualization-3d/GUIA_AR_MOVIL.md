# 📱 Guía Rápida - AR.js con Cámara Real

## 🎯 Cómo Usar en tu Celular

### **1. Preparar el Marcador**
- Abre en tu celular: http://localhost:5173/markers/index.html
- O imprime el marcador Hiro desde tu computadora

### **2. Acceder desde tu Celular**

#### **Opción A: Usando tu IP local**
```bash
# En tu Mac, encuentra tu IP:
ifconfig | grep "inet " | grep -v 127.0.0.1
```

Luego en tu celular abre:
```
http://TU_IP_LOCAL:5173/
```
Ejemplo: `http://192.168.1.10:5173/`

#### **Opción B: Usando ngrok (recomendado para HTTPS)**
```bash
# Instalar ngrok:
brew install ngrok

# En otra terminal, crear túnel:
ngrok http 5173
```

Ngrok te dará una URL HTTPS como:
```
https://abc123.ngrok.io
```

Abre esa URL en tu celular.

### **3. Usar el AR**
1. Abre la URL en el navegador de tu celular (Chrome/Safari)
2. Permite acceso a la cámara cuando lo pida
3. Haz clic en **"Activar AR"** 📱
4. Apunta la cámara al marcador Hiro
5. Los objetos 3D aparecerán sobre el marcador

## ⚠️ Requisitos Importantes

### **En Celular:**
- ✅ Android: Chrome, Firefox, Edge
- ✅ iOS: Safari (iOS 11+)
- ✅ Conexión a la misma red WiFi (si usas IP local)
- ✅ HTTPS obligatorio en iOS (usa ngrok)

### **Permisos:**
- Cámara trasera activada
- Permitir acceso a cámara en el navegador
- Ubicación (algunos navegadores la piden)

## 🐛 Solución de Problemas

### **"No se puede acceder a la cámara"**
✅ Verifica permisos del navegador:
- Chrome: Configuración → Privacidad → Cámara
- Safari: Configuración → Safari → Cámara

### **"Pantalla negra"**
✅ Asegúrate de estar en HTTPS (usa ngrok)
✅ Recarga la página
✅ Verifica que ARjs.js se cargó (abre consola)

### **"No detecta el marcador"**
✅ Buena iluminación (sin sombras fuertes)
✅ Marcador plano (sin arrugas)
✅ Mantén distancia de 20-50cm
✅ Marcador completamente visible
✅ Borde negro continuo y nítido

## 📊 Logs de Debug

Abre la consola del navegador para ver:
```
✅ Cámara inicializada
✅ AR Context inicializado
✅ Video posicionado correctamente
✅ Marcador Hiro detectado!
```

## 🎨 Objetos que Aparecerán

Cuando detecte el marcador verás:
- 🟦 Cubo azul central
- 🔴 Esfera roja flotante
- 🟢 Torus verde
- 🟡 Cono amarillo
- ⚫ Sombras proyectadas
- 🟢 Indicador verde cuando marcador visible

## 🚀 Prueba Rápida en Computadora

Si tienes webcam en tu Mac:
```bash
npm run dev
# Abre: http://localhost:5173/
# Clic en "Activar AR"
# Muestra el marcador a la webcam
```

---

**¿Listo para probar?** 🎉
