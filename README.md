# onion-architecture-fastapi
Onion Architecture 

## FEATURES

- SQL ALCHEMY2
- Alembic for DB Migration
- Pydantic2 schema

### 1. Clone the repo

- https://github.com/SonuGeorge-Experion/onion-architecture-fastapi.git
- switch to development brach 

### 2. Create a virtual environment

- python -m venv venv
- source venv/bin/activate  # Ubuntu 
- venv\Scripts\activate # Windows

### 3. Install dependencies

- pip install -r requirements.txt

### 4. Run the app

- uvicorn app.main:app --reload  # local
- uvicorn app.main:app --host 0.0.0.0 --port <port-address> --workers <no-of-wrokers> # dev/prod
- gunicorn app.main:app \
    -k uvicorn.workers.UvicornWorker \
    -w <no-of-workers> \
    -b 0.0.0.0:<port-address>  # with gunicorn 

### 5. Migrations (Alembic)

- alembic init app/infrastructure/db/migrations # alembic one-time setup
- alembic check || alembic revision --autogenerate -m "Initial" # make migration file
- alembic upgrade head # migration

### 6. Script Execution
python -m app.scripts.<file_name_without_ext>

## 7. Onion Architecture

```text

app/
│
├── domain/                        # Core Business Layer (NO external deps)
│   ├── entities/                  # Business objects
│   │   ├── donor.py
│   │   ├── process.py
│   │   └── resources.py
│   │
│   ├── value_objects/             # Immutable small objects
│   │   └── donor_znumber.py
│   │
│   ├── repositories/              # Repository interfaces
│   │   ├── donor_repository.py
│   │   └── process_repository.py
│   │
│   ├── services/                  # Domain services (pure business logic)
│   │   ├── process_approval.py
│   │   └── 
│   │
│   └── exceptions/                # Domain-specific exceptions
│       └── domain_exceptions.py
│
├── application/                   # Use Case Layer
│   ├── use_cases/
│   │   └── donor.py
│   │
│   ├── dtos/                      # Data transfer between layers
│       ├── donor.py
│   
│
├── infrastructure/                # External Systems Layer
│   ├── db/
│   │   ├── models/                # SQLAlchemy models
│   │   │   ├── donor.py
│   │   │
│   │   ├── repositories/          # Repo implementations
│   │   │   ├── base_repository.py
│   │   │   └── donor_repository.py
│   │   │
│   │   ├── migrations/          # alembic migrations
│   │   │   ├── versions/
│   │   │
│   │   │
│   │   ├── session.py
│   │   ├── base_class.py
│   │   ├── base.py
│   │   └── utils.py
│   │
│   ├── external_services/         # 3rd-party integrations
│   │   ├── email_service.py
│   │   ├── digital_signature.py
│   │   
│   │
│   ├── messaging/                 # Service Bus, RabbitMQ etc
│   │   └── service_bus.py
│   │
│   └── config/
│       └── settings.py
│
├── api/                           # Presentation Layer (FastAPI)
│   ├── v1/routers/
│   │   ├── donors.py
│   │   └── process.py
│   |
│   ├── routes.py
│   │
│   ├── schemas/                   # Pydantic models
│   │   ├── donor.py
│   │   └── process.py
│   │
│   ├── dependencies/
│   │   └── auth_dependency.py
│   │
│   └── middleware/
│       └── logging_middleware.py
│
├── core/                          # Shared utilities
│   ├── security.py
│   ├── config.py
│   └── constants.py
│
├── tests/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── api/
│
└── main.py                        # FastAPI entry point

```