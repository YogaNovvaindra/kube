# Money

Money is a personal finance management application for tracking expenses, budgets, and accounts.

## Components

- **[`money.yml`](./money/money.yml)**: Deployment manifest for the core application.
- **[`money-cred.yml`](./money/money-cred.yml)**: Sealed credentials for the application database.

## Deployment

The application is deployed via Argo CD and connects to a dedicated PostgreSQL instance.
