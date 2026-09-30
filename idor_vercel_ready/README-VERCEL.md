# Vercel deployment

These folders keep the original challenge server code unchanged.

Added files:
- `Dockerfile.vercel` — Vercel container deployment entry.
- `index.html` — standalone front-end copy; it does not replace `server.py`.

## Deploy one challenge per Vercel project

Upload one challenge folder to its own GitHub repository, then import that repository into Vercel.

The repository root should contain:
- `Dockerfile.vercel`
- `Dockerfile`
- `server.py`
- `requirements.txt` (path traversal)
- `index.html`

Do not set the project as a static-site deployment. Vercel should detect the container from `Dockerfile.vercel`.

The application already reads `PORT` from the environment, which is required for the Vercel container.

## Important

The HTML file is only a front-end copy. The actual vulnerability and flag logic remain in `server.py`.
