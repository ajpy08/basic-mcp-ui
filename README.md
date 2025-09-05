# Calculadora MCP con Interfaz Web

Este proyecto implementa un servidor MCP (Model Context Protocol) con una interfaz web moderna para realizar operaciones matemáticas básicas.

## Características

- ✅ Servidor MCP con herramientas de cálculo (suma, resta, multiplicación, división)
- ✅ Interfaz web moderna y responsive
- ✅ Historial de operaciones
- ✅ Manejo de errores (división por cero)
- ✅ Validación de entrada
- ✅ Diseño atractivo con gradientes y animaciones

## Estructura del Proyecto

```
javi-test-mcp-ui/
├── main.py                # Archivo principal (ejecuta ambos servidores)
├── server.py              # Servidor MCP (solo herramientas)
├── proxy.py               # Servidor web proxy (interfaz web)
├── static/
│   ├── index.html         # Interfaz web principal
│   ├── style.css          # Estilos CSS
│   └── script.js          # Lógica JavaScript
├── .env                   # Variables de entorno
├── .env.example           # Plantilla de variables de entorno
├── requirements.txt       # Dependencias Python
└── README.md              # Este archivo
```

## Instalación y Uso

1. **Clonar el repositorio**:
   ```bash
   git clone <url-del-repositorio>
   cd javi-test-mcp-ui
   ```

2. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configurar variables de entorno** (opcional):
   ```bash
   cp .env.example .env
   # Editar .env con tus configuraciones personalizadas
   ```

4. **Ejecutar los servidores**:
   
   **Opción A: Ejecutar ambos servidores juntos (recomendado)**
   ```bash
   python main.py
   ```
   
   **Opción B: Ejecutar servidores por separado**
   ```bash
   # Terminal 1 - Servidor MCP
   python server.py
   
   # Terminal 2 - Servidor Proxy Web
   python proxy.py
   ```

5. **Acceder a la interfaz web**:
   - Abre tu navegador y ve a: `http://127.0.0.1:8001` (o el puerto configurado)
   - El servidor MCP estará disponible en: `http://127.0.0.1:8000` (o el puerto configurado)

## Funcionalidades

### Servidor MCP
- **Puerto**: 8000
- **Herramientas disponibles**:
  - `add(x, y)`: Suma dos números
  - `subtract(x, y)`: Resta dos números
  - `multiply(x, y)`: Multiplica dos números
  - `divide(x, y)`: Divide dos números (con validación de división por cero)

### Interfaz Web
- **Puerto**: 8001
- **Características**:
  - Interfaz intuitiva con campos de entrada para dos números
  - Botones para cada operación matemática
  - Visualización del resultado en tiempo real
  - Historial de las últimas 10 operaciones
  - Manejo de errores con mensajes informativos
  - Diseño responsive que se adapta a diferentes tamaños de pantalla

## Configuración

El proyecto utiliza variables de entorno para la configuración. Puedes modificar el archivo `.env` para personalizar:

### Variables Disponibles

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `HOST_MCP` | Host del servidor MCP | `127.0.0.1` |
| `PORT_MCP` | Puerto del servidor MCP | `8000` |
| `HOST_UI` | Host de la interfaz web | `127.0.0.1` |
| `PORT_UI` | Puerto de la interfaz web | `8001` |
| `LOG_LEVEL` | Nivel de logging | `INFO` |
| `LOG_FORMAT` | Formato de los logs | `%(levelname)s \| %(name)s \| %(message)s` |
| `APP_NAME` | Nombre de la aplicación | `Calculator Server` |
| `STATIC_DIR` | Directorio de archivos estáticos | `static` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS | `*` |
| `CORS_METHODS` | Métodos HTTP permitidos | `GET,POST,OPTIONS` |
| `CORS_HEADERS` | Headers permitidos | `Content-Type` |

### Ejemplo de Configuración

```bash
# .env
HOST_MCP=0.0.0.0
PORT_MCP=8000
HOST_UI=0.0.0.0
PORT_UI=8001
LOG_LEVEL=DEBUG
```

## Tecnologías Utilizadas

- **Backend**: Python, FastMCP
- **Frontend**: HTML5, CSS3, JavaScript (ES6+)
- **Servidor Web**: HTTP Server nativo de Python
- **Protocolo**: MCP (Model Context Protocol)
- **Configuración**: python-dotenv

## Arquitectura

El proyecto está dividido en tres componentes principales:

### 1. **server.py** - Servidor MCP Puro
- Contiene únicamente las herramientas MCP (`add`, `subtract`, `multiply`, `divide`)
- Funciones core de cálculo (`add_numbers`, `subtract_numbers`, etc.)
- Wrappers MCP que exponen las funciones core
- Ejecuta el servidor MCP en el puerto configurado

### 2. **proxy.py** - Servidor Web Proxy
- Maneja todas las peticiones HTTP de la interfaz web
- Sirve archivos estáticos (HTML, CSS, JS)
- Endpoint `/call_tool` que actúa como proxy para las herramientas MCP
- Importa y llama directamente a las funciones core del servidor MCP
- Maneja CORS y configuración

### 3. **main.py** - Orquestador
- Ejecuta ambos servidores simultáneamente
- Servidor MCP en un hilo separado
- Servidor proxy web en el hilo principal

### Flujo de Comunicación

```
┌─────────────────┐    HTTP     ┌─────────────────┐    Import    ┌─────────────────┐
│   Interfaz Web  │ ──────────► │  proxy.py       │ ──────────► │  server.py      │
│   (Frontend)    │             │  (Puerto 8001)  │             │  (Funciones)    │
└─────────────────┘             └─────────────────┘             └─────────────────┘
                                         │
                                         │ MCP Protocol
                                         ▼
                                ┌─────────────────┐
                                │  server.py      │
                                │  (Puerto 8000)  │
                                └─────────────────┘
```

## Desarrollo

La separación de responsabilidades permite:
- **Mantenimiento más fácil**: Cada archivo tiene una responsabilidad específica
- **Escalabilidad**: Puedes ejecutar servidores por separado si es necesario
- **Claridad**: El código MCP está separado del código web
- **Reutilización**: Las funciones core pueden ser importadas por otros módulos

## Personalización

Puedes modificar fácilmente:
- **Estilos**: Edita `static/style.css`
- **Funcionalidad**: Modifica `static/script.js`
- **Herramientas MCP**: Añade nuevas funciones en `server.py`
- **Interfaz**: Personaliza `static/index.html`
