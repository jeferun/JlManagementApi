# API de Gestión de Afiliados (JlManagementApi)

## 📌 Descripción del Proyecto
Este proyecto proporciona una API REST diseñada para registrar afiliados y gestionar sus aportes mensuales. Permite llevar un control histórico de las contribuciones financieras de cada persona, así como consultar un resumen agregado (total aportado, cantidad de aportes y fecha de última contribución) de forma eficiente.

## 🛠️ Tecnologías Utilizadas
- **Python 3.9+**
- **Django 4.2 LTS**
- **Django REST Framework (DRF)**
- **PostgreSQL** (para la persistencia principal en Docker)
- **SQLite** (como fallback para desarrollo rápido local)
- **Docker & Docker Compose**

## 🏗️ Arquitectura y Decisiones de Diseño
El proyecto fue construido bajo un enfoque estricto de **Clean Architecture**, incorporando conceptos de **Domain-Driven Design (DDD)** y principios **SOLID**.

La motivación detrás de esta decisión es garantizar que las reglas de negocio base estén **completamente aisladas** del framework web (Django) y de la base de datos. Para lograrlo, la lógica se dividió en cuatro capas independientes:

1. **Domain (Capa de Dominio):** Contiene contratos (interfaces abstractas) y excepciones puras de negocio. **Regla de oro aplicada:** En la carpeta `domain/` hay 0 imports de Django o de DRF.
2. **Application (Casos de Uso):** Son orquestadores de Python puro (como `RegisterContribution` o `CreateAffiliate`). Agrupan las validaciones requeridas del negocio (ej. que un aporte sea mayor a 0 o que un afiliado esté "ACTIVE"). Reciben repositorios de infraestructura dinámicamente mediante **Inyección de Dependencias**.
3. **Infrastructure (Capa de Infraestructura):** Implementa el ORM de Django (`models.py`) y los repositorios concretos. Estos repositorios ejecutan las sentencias SQL y atrapan errores de base de datos (`IntegrityError`, `ObjectDoesNotExist`), traduciéndolos a Excepciones del Dominio para no propagar código técnico al negocio.
4. **API (Capa de Presentación):** Utiliza DRF (`ViewSets` y `Serializers`). Su única tarea es procesar las requests HTTP, deserializar el JSON, delegar el trabajo a los Casos de Uso y retornar respuestas 200/201. Contiene un **manejador global de excepciones** que transforma los errores de negocio puros en códigos de error HTTP estructurados (400, 404).

## 🚀 Pasos para levantar el backend (Desarrollo Local sin Docker)

1. **Crear y activar el entorno virtual:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # En macOS/Linux
   # En Windows: venv\Scripts\activate
   ```
2. **Instalar dependencias:**
   ```bash
   pip install --upgrade pip
   ```
3. **Ejecutar migraciones (usa SQLite por defecto si no se detectan env vars):**
   ```bash
   python manage.py migrate
   ```
4. **Correr el servidor local:**
   ```bash
   python manage.py runserver
   ```
El servidor estará corriendo en `http://127.0.0.1:8000/`.

## 🐋 Pasos para levantar todo con Docker

La dockerización asegura un entorno idéntico para desarrollo y producción conectando la API con una base de datos PostgreSQL robusta.

1. **Generar el archivo de entorno:**
   ```bash
   cp .env.example .env
   ```
2. **Construir y levantar los contenedores en segundo plano:**
   ```bash
   docker-compose up --build -d
   ```
3. **Ejecutar las migraciones de la base de datos:**
   ```bash
   docker-compose exec web python manage.py migrate
   ```
La API estará lista y escuchando en `http://localhost:8000/api/`.

## 📡 Endpoints de la API

La API expone los siguientes endpoints principales:

### Afiliados
- `GET /api/affiliates/`: Listar todos los afiliados (soporta paginación y filtros `?full_name=` y `?status=`).
- `POST /api/affiliates/`: Registrar un nuevo afiliado.
- `GET /api/affiliates/{id}/`: Obtener detalles de un afiliado.
- `PUT /api/affiliates/{id}/`: Actualizar un afiliado completamente.
- `PATCH /api/affiliates/{id}/`: Actualizar parcialmente un afiliado (ej. cambiar status a INACTIVE).
- `DELETE /api/affiliates/{id}/`: Eliminación lógica (soft delete) de un afiliado.

### Aportes
- `POST /api/contributions/`: Registrar un nuevo aporte asociado a un afiliado.
- `DELETE /api/contributions/{id}/`: Eliminación lógica (soft delete) de un aporte.

### Reportes y Resúmenes
- `GET /api/affiliates/{id}/summary/`: Obtener el resumen de un afiliado (total aportado, cantidad de aportes, último aporte).
- `GET /api/affiliates/{id}/contributions/`: Obtener el historial de aportes de un afiliado específico.
- `GET /api/affiliates/dashboard-summary/`: Obtener el dashboard global de todos los afiliados y aportes.

## 🚀 Pruebas con Postman

Para facilitar las pruebas de los endpoints, se ha incluido una colección de Postman en la raíz del proyecto.

1. Abre **Postman**.
2. Ve a **Import** o presiona `Ctrl+O` / `Cmd+O`.
3. Selecciona el archivo [`JlManagement_Postman_Collection.json`](./JlManagement_Postman_Collection.json) que se encuentra en la raíz del proyecto.
4. Una vez importada, verás la colección **JlManagement API** con todos los endpoints configurados y listos para ejecutar.
5. La colección ya incluye una variable `base_url` configurada por defecto a `http://localhost:8000`.
