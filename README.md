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

### Ejecutar el Proceso de Ingesta (CLI)
Para correr el scraper y parsear los datos del currículum, ejecuta el comando CLI desde la raíz del proyecto:

```bash
python -m app.infrastructure.cli.ingest_curriculum
```

El script de ingesta inicializa el esquema de base de datos y ejecuta el flujo utilizando las configuraciones declaradas en el archivo `.env`.

## Principios SOLID Aplicados

Este proyecto está diseñado siguiendo rigurosamente los principios SOLID para garantizar mantenibilidad, extensibilidad y testabilidad:

1. **S - Single Responsibility Principle (Principio de Responsabilidad Única)**
   - Cada clase y módulo tiene una única razón para cambiar.
   - Las entidades del dominio solo definen datos de negocio. Los casos de uso orquestan lógica, y los adaptadores se encargan únicamente del detalle tecnológico (HTTP, base de datos, scrapers).

2. **O - Open/Closed Principle (Principio de Abierto/Cerrado)**
   - El código está abierto a la extensión pero cerrado a la modificación.
   - La selección de convertidores de PDF (`PDFConverter`) o modelos de lenguaje (`LLMModelFactory`) se realiza a través de fábricas y proveedores dinámicos basados en la configuración, permitiendo agregar nuevos proveedores sin alterar la lógica de negocio core.

3. **L - Liskov Substitution Principle (Principio de Sustitución de Liskov)**
   - Las subclases o implementaciones de interfaces deben poder sustituir a sus clases base sin alterar el comportamiento correcto del programa.
   - Todas las implementaciones de los puertos externos (como `SqlCurriculumRepositoryAdapter` para `CurriculumRepository`) respetan la firma y el contrato formal definido en el dominio.

4. **I - Interface Segregation Principle (Principio de Segregación de Interfaces)**
   - Los clientes no deben verse obligados a depender de interfaces que no utilizan.
   - Se utilizan protocolos de Python (`typing.Protocol`) pequeños y específicos para cada puerto de salida (`ContentDownloader`, `PDFConverter`, `CurriculumRepository`, etc.), asegurando contratos minimalistas y limpios.

5. **D - Dependency Inversion Principle (Principio de Inversión de Dependencias)**
   - Los módulos de alto nivel no deben depender de módulos de bajo nivel; ambos deben depender de abstracciones.
   - La capa de dominio define interfaces (puertos) para interactuar con bases de datos o servicios externos, y la capa de infraestructura implementa dichas interfaces (adaptadores) que son inyectadas en tiempo de ejecución.
