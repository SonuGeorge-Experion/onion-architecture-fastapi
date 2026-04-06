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
#### UV 
- uv venv --python 3.12
- uv add -r requirements.txt # Dont execute it if there is no requirement change
- uv sync # uses uv.lock
- uv run uvicorn app.main:app --reload
- uv run alembic upgrade head 

#### PIP MANAGER

- python -m venv venv
- source venv/bin/activate  # Ubuntu 
- venv\Scripts\activate # Windows

### 3. Install dependencies

- pip install -r requirements.txt

### 4. VS Code Workspace Settings

Add the following to your `.vscode/settings.json` file to enable Ruff integration:

```json
{
  "editor.formatOnSave": true,
  "[python]": {
    "editor.defaultFormatter": "charliermarsh.ruff"
  },
  "editor.codeActionsOnSave": {
    "source.fixAll.ruff": "explicit"
  },
  "editor.formatOnPaste": true,
  "editor.rulers": [88],
  "files.trimTrailingWhitespace": true
}
```
- Rerun the tool manually to update the settings and pyproject.toml file
``` Bash
ruff check .
```

### 4. Precommit hook

- Install the hook defined in `.pre-commit-config.yaml` into your Git repos `.git/hooks` directory
``` Bash
pre-commit install
```
- Run hooks manually on all files
``` Bash
pre-commit run --all-files
```
- Update hooks to the latest version
``` Bash
pre-commit autoupdate
```
- Skip hook for a commit
``` Bash
git commit -m "hotfix: code change" --no-verify
```
### 4. Security Scan 
- Bandit
``` Bash
pre-commit run bandit --all-files
```

### 4. Run the app

#### Without Docker

- uvicorn app.main:app --reload  # local
- uvicorn app.main:app --host 0.0.0.0 --port `<port-address>` --workers `<no-of-wrokers>` # dev/prod
- gunicorn app.main:app \
    -k uvicorn.workers.UvicornWorker \
    -w `<no-of-workers>` \
    -b 0.0.0.0:`<port-address>`  # with gunicorn 


#### With Docker in local 

- docker build -t fastapi-app .
- docker build -f Dockerfile.dev -t fastapi-app . # Dockerfile with extension 
- docker run -d -it --net=host fastapi-app # for same netwrok as that of host (local run)
- docker run -it -p 8000:8000 fastapi-app # if not same network as that of host
- docker ps # active conatiner
- docker ps -a # all containers
- docker start `<conatiner_id>` # start docker
- docker stop `<container_id>` # stop docker
- docker start -ai `<container_id>` # start the container with terminal log
- docker logs `<container_id>` # for logs
- docker rm `<container_id>` # remove a stopped conatiner
- docker images # list all images
- docker rmi `<image_id>` # remove a docker image


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