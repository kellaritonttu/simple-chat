# Alembic Configuration

Contains the initial database schema for the service, starting from release `v0.1.0`.

## Tables

- `users`
- `messages`

## Seed Data

Inserts an `Anonymous` user into `users` as the default user for messages.
This allows message rows created before user accounts existed to reference a
valid user, enabling a smooth migration between `v0.1.0` and `v0.2.0`.

## Migration Policy

Schema and seed changes are applied **manually** via a Cloud Run job that runs table creation + the `Anonymous` user insert..

## TODO

- Automate `alembic upgrade head` execution as part of the deploy pipeline 
  once data migrations are introduced.