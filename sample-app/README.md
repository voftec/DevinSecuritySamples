# sample-app — Aplicación intencionalmente vulnerable

> **Aviso**: esta app es solo para fines educativos en el workshop de seguridad. No desplegar en producción.

## Vulnerabilidades esperadas

1. SQL injection en `/login` (concatenación de strings en query).
2. IDOR / broken access control en `/admin/users/<id>` (sin validación de rol).
3. Path traversal en `/files` (uso directo del parámetro `name` en `send_file`).
4. Hardcoded weak credentials (`admin` / `password123`).

## Ejecutar

```bash
source ../.venv/bin/activate
python app.py
```

## Endpoints

- `GET /`
- `POST /login` con `username` y `password`
- `GET /admin/users/<id>`
- `GET /files?name=...`
- `GET /health`
