# Harbor

Harbor is an open-source trusted cloud native registry project that stores, signs, and scans content.

## Components

- **`core.yml`**: Core Harbor service and API.
- **`registry.yml`**: Container registry storage service.
- **`harbor/db/postgres.yml`**: PostgreSQL database for Harbor.
- **`harbor/db/valkey.yml`**: Valkey (Redis) for Harbor.
- **`nginx.yml`**: Internal proxy for Harbor components.
- **`jobservices.yml`**: Handles background tasks like replication and scanning.
- **`trivy.yml`**: Integrated vulnerability scanner.
- **`harbor/db/backup.yml`**: Automated backup jobs for the database.

## Usage

Harbor is used to host custom images and proxy public registries to improve pull speeds and security.
