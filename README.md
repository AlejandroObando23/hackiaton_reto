"# 🏥 MediByte - Chatbot Médico Inteligente

> Una solución de IA conversacional para consultas médicas y gestión de seguros de salud

![Status](https://img.shields.io/badge/status-active-success) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-green) ![React](https://img.shields.io/badge/react-19-blue)

## 📋 Descripción

**MediByte** es una plataforma integral que combina inteligencia artificial con información médica y de seguros de salud. Permite a los usuarios:

- 💬 **Chatear con IA** sobre síntomas, medicamentos y procedimientos médicos
- 🖼️ **Análisis de imágenes médicas** mediante detección de IA
- 👤 **Gestión de perfil** personalizado con historial médico
- 🔐 **Autenticación segura** con JWT y encriptación
- 📚 **Base de conocimiento** sobre pólizas de seguros

## 🎯 Características Principales

✨ **Backend Robusto**
- API REST con FastAPI
- LLM de Groq integrado vía LangChain
- Base de datos MongoDB
- Búsqueda vectorial con ChromaDB
- Procesamiento de documentos médicos

✨ **Frontend Moderno**
- Interfaz React con Vite
- Chat en tiempo real
- Sidebar informativa
- Diseño responsivo
- Iconografía con Lucide React

✨ **Seguridad**
- Autenticación JWT
- Hashing bcrypt de contraseñas
- Validación de entrada con Pydantic
- CORS configurado

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.9+
- Node.js 18+
- MongoDB
- API Key de Groq

### Instalación del Backend

```bash
cd backend
pip install -r requirements.txt
```

Crea un archivo `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
GROQ_API_KEY=tu_clave_groq_aqui
JWT_SECRET=tu_secreto_jwt_aqui
```

Inicia el servidor:
```bash
python main.py
```

El API estará disponible en `http://localhost:8000`

### Instalación del Frontend

```bash
cd frontend
npm install
npm run dev
```

La interfaz estará disponible en `http://localhost:5173`

## 📦 Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **LangChain** - Orquestación de modelos de IA
- **Groq** - LLM rápido en la nube
- **MongoDB** - Base de datos NoSQL
- **ChromaDB** - Base de datos vectorial
- **Motor** - Driver asincrónico de MongoDB

### Frontend
- **React 19** - Librería de UI
- **Vite** - Build tool ultrarrápido
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos SVG

## 📁 Estructura del Proyecto

```
hackiaton_reto/
├── backend/
│   ├── models/          # Modelos de datos (User, MedicalBot, ImageDetection)
│   ├── routers/         # Endpoints de la API
│   ├── services/        # Lógica de negocio
│   ├── database/        # Conexión a MongoDB
│   ├── utils/           # Utilidades (email, hashing, seguridad)
│   ├── ChatbotData/     # Datos de entrenamiento
│   ├── chroma_db_v2/    # Índice vectorial
│   └── main.py          # Entrada principal
│
├── frontend/
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── App.jsx      # Aplicación principal
│   │   └── main.jsx     # Entry point
│   └── package.json
│
└── Dockerfile           # Contenerización
```

## 🔧 Configuración

### Variables de Entorno

**Backend** (`.env`):
```env
MONGODB_URL=           # URI de conexión MongoDB
GROQ_API_KEY=          # Clave de API de Groq
JWT_SECRET=            # Secreto para tokens JWT
JWT_ALGORITHM=HS256    # Algoritmo de firma
SMTP_SERVER=           # Servidor SMTP para emails
SMTP_PORT=             # Puerto SMTP
```

## 📖 Uso

### Chat con la IA Médica
```bash
POST /api/chat
{
  "message": "¿Cuáles son los síntomas de la gripe?",
  "user_id": "12345"
}
```

### Análisis de Imagen
```bash
POST /api/analyze-image
{
  "image": "<base64_encoded_image>",
  "user_id": "12345"
}
```

### Autenticación
```bash
POST /api/auth/register
POST /api/auth/login
```

## 🐳 Docker

Construye y ejecuta con Docker:
```bash
docker build -t medibyte .
docker run -p 8000:8000 -p 5173:5173 medibyte
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios principales:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

¿Problemas? Abre un issue o contacta al equipo de desarrollo.

---

**Hecho con ❤️ para hackathons de IA**Chatbot Médico Inteligente

> Una solución de IA conversacional para consultas médicas y gestión de seguros de salud

![Status](https://img.shields.io/badge/status-active-success) ![License](https://img.shields.io/badge/license-MIT-blue) ![Python](https://img.shields.io/badge/python-3.9+-green) ![React](https://img.shields.io/badge/react-19-blue)

## 📋 Descripción

**MediByte** es una plataforma integral que combina inteligencia artificial con información médica y de seguros de salud. Permite a los usuarios:

- 💬 **Chatear con IA** sobre síntomas, medicamentos y procedimientos médicos
- 👤 **Gestión de perfil** personalizado con historial médico
- 🔐 **Autenticación segura** con JWT y encriptación
- 📚 **Base de conocimiento** sobre pólizas de seguros

## 🎯 Características Principales

✨ **Backend Robusto**
- API REST con FastAPI
- LLM de Groq integrado vía LangChain
- Base de datos MongoDB
- Búsqueda vectorial con ChromaDB
- Procesamiento de documentos médicos

✨ **Frontend Moderno**
- Interfaz React con Vite
- Chat en tiempo real
- Sidebar informativa
- Diseño responsivo
- Iconografía con Lucide React

✨ **Seguridad**
- Autenticación JWT
- Hashing bcrypt de contraseñas
- Validación de entrada con Pydantic
- CORS configurado

## 🚀 Inicio Rápido

### Requisitos Previos
- Python 3.9+
- Node.js 18+
- MongoDB
- API Key de Groq

### Instalación del Backend

```bash
cd backend
pip install -r requirements.txt
```

Crea un archivo `.env`:
```env
MONGODB_URL=mongodb://localhost:27017
GROQ_API_KEY=tu_clave_groq_aqui
JWT_SECRET=tu_secreto_jwt_aqui
```

Inicia el servidor:
```bash
python main.py
```

El API estará disponible en `http://localhost:8000`

### Instalación del Frontend

```bash
cd frontend
npm install
npm run dev
```

La interfaz estará disponible en `http://localhost:5173`

## 📦 Stack Tecnológico

### Backend
- **FastAPI** - Framework web moderno y rápido
- **LangChain** - Orquestación de modelos de IA
- **Groq** - LLM rápido en la nube
- **MongoDB** - Base de datos NoSQL
- **ChromaDB** - Base de datos vectorial
- **Motor** - Driver asincrónico de MongoDB

### Frontend
- **React 19** - Librería de UI
- **Vite** - Build tool ultrarrápido
- **Axios** - Cliente HTTP
- **Lucide React** - Iconos SVG

## 📁 Estructura del Proyecto

```
hackiaton_reto/
├── backend/
│   ├── models/          # Modelos de datos (User, MedicalBot, ImageDetection)
│   ├── routers/         # Endpoints de la API
│   ├── services/        # Lógica de negocio
│   ├── database/        # Conexión a MongoDB
│   ├── utils/           # Utilidades (email, hashing, seguridad)
│   ├── ChatbotData/     # Datos de entrenamiento
│   ├── chroma_db_v2/    # Índice vectorial
│   └── main.py          # Entrada principal
│
├── frontend/
│   ├── src/
│   │   ├── components/  # Componentes React
│   │   ├── App.jsx      # Aplicación principal
│   │   └── main.jsx     # Entry point
│   └── package.json
│
└── Dockerfile           # Contenerización
```

## 🔧 Configuración

### Variables de Entorno

**Backend** (`.env`):
```env
MONGODB_URL=           # URI de conexión MongoDB
GROQ_API_KEY=          # Clave de API de Groq
JWT_SECRET=            # Secreto para tokens JWT
JWT_ALGORITHM=HS256    # Algoritmo de firma
SMTP_SERVER=           # Servidor SMTP para emails
SMTP_PORT=             # Puerto SMTP
```

## 📖 Uso

### Chat con la IA Médica
```bash
POST /api/chat
{
  "message": "¿Cuáles son los síntomas de la gripe?",
  "user_id": "12345"
}
```

### Análisis de Imagen
```bash
POST /api/analyze-image
{
  "image": "<base64_encoded_image>",
  "user_id": "12345"
}
```

### Autenticación
```bash
POST /api/auth/register
POST /api/auth/login
```

## 🐳 Docker

Construye y ejecuta con Docker:
```bash
docker build -t medibyte .
docker run -p 8000:8000 -p 5173:5173 medibyte
```

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Para cambios principales:
1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Añade mejora'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la licencia MIT. Ver [LICENSE](LICENSE) para más detalles.

## 📞 Soporte

¿Problemas? Abre un issue o contacta al equipo de desarrollo.

---

**Hecho con ❤️ para hackathons de IA**" 
