# p12nt-svc-curriculum-service

Servicio backend de **curriculum** en la plataforma **12NT**.

## Arquitectura
Este servicio sigue la **Arquitectura Hexagonal (Ports & Adapters)** para garantizar un desacoplamiento absoluto de las tecnologías y protocolos de comunicación frente al núcleo de negocio:
- **app/domain**: Entidades puras y puertos (interfaces de entrada y salida). No depende de FastAPI, SQLModel ni librerías externas de persistencia/red.
- **app/application**: Casos de uso e implementaciones de negocio orquestando los puertos.
- **app/infrastructure**: Adaptadores específicos para bases de datos (SQLModel con PostgreSQL), API Web (FastAPI) e integración de eventos.

## Requisitos de Ejecución
- Python 3.14 o superior.
- Gestor de paquetes **uv** (Astral).
- PostgreSQL.

### Correr localmente con uv
1. Inicializar el entorno virtual y sincronizar dependencias de forma automática:
   ```bash
   uv sync
   ```
2. Activar el entorno virtual:
   - En Windows (PowerShell):
     ```powershell
     .venv\Scripts\Activate.ps1
     ```
   - En Linux/macOS:
     ```bash
     source .venv/bin/activate
     ```
3. Ejecutar la aplicación:
   ```bash
   python app/main.py
   ```
4. Acceder al Swagger de documentación en: [http://localhost:8000/docs](http://localhost:8000/docs)
