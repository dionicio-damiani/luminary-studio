# Luminary Studio

A production-ready, fully responsive landing page template for service businesses — built with pure HTML/CSS/JS and a FastAPI backend. Ships with **Luminary Studio** as demo content (fictional interior design studio).

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)
[![Tests](https://github.com/dionicio-damiani/business-landing-page/actions/workflows/tests.yml/badge.svg)](https://github.com/dionicio-damiani/business-landing-page/actions/workflows/tests.yml)

## Live Demo

**[→ Try it live](https://luminary-studio.up.railway.app)**

![Preview](static/img/og-cover.gif)

---

## Features

- **8 complete sections** — Navbar, Hero, Services, Portfolio, Process, Testimonials, Contact, Footer
- **Fully responsive** — tested from 320px to 1440px+
- **Zero frontend frameworks** — custom CSS, vanilla JS
- **Shared validation messages** — defined once in Python, injected into the page for client + API parity
- **Contact API** — `POST /api/contact` with Pydantic + `email-validator`
- **Health check** — `GET /health` for deployments
- **Accessible** — semantic HTML, ARIA, keyboard navigable

---

## Quick start

**Requirements:** Python 3.11+

```bash
git clone https://github.com/dionicio-damiani/business-landing-page.git
cd business-landing-page

python -m venv venv

# Windows (PowerShell)
venv\Scripts\Activate.ps1
# macOS / Linux
source venv/bin/activate

pip install -r requirements.txt

python main.py
```

Open [http://localhost:8000](http://localhost:8000). API docs: [http://localhost:8000/docs](http://localhost:8000/docs).

Stop the server with `Ctrl+C`.

### Environment variables

Copy `.env.example` to `.env` and adjust if needed (optional):

| Variable   | Default   | Description                                      |
|-----------|-----------|--------------------------------------------------|
| `SITE_URL` | _(empty)_ | Public URL for `canonical` / Open Graph tags     |
| `HOST`    | `0.0.0.0` | Bind address                                     |
| `PORT`    | `8000`    | Port                                             |
| `RELOAD`  | `true`    | Auto-reload (set `false` in production)          |
| `RESEND_API_KEY` | _(empty)_ | [Resend](https://resend.com) API key — leave blank to log submissions to console only |
| `CONTACT_EMAIL` | `hello@luminarystudio.com` | Inbox that receives contact form submissions |

Variables in `.env` are loaded automatically via `python-dotenv`. You can also set them in your shell or a process manager — both are read via `os.getenv`.

**Production example:**

```bash
RELOAD=false PORT=8000 python main.py
# or
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## Project structure

```
business-landing-page/
├── .github/
│   └── workflows/tests.yml  # CI: runs the pytest suite
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routes, static/templates
│   ├── schemas.py       # ContactForm validation
│   └── messages.py      # Shared copy (validation + success text)
├── static/
│   ├── css/styles.css
│   ├── img/og-cover.gif
│   └── js/app.js        # Reads validation rules from #app-config
├── templates/
│   ├── index.html
│   └── 404.html
├── tests/
│   └── test_main.py     # pytest suite (httpx TestClient)
├── main.py              # Single entry point (uvicorn)
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── Procfile             # Railway deploy
├── .env.example
└── .gitignore
```

---

## API

| Method | Path            | Description                    |
|--------|-----------------|--------------------------------|
| GET    | `/`             | Landing page (Jinja2)          |
| GET    | `/health`       | `{"status": "ok"}`             |
| GET    | `/robots.txt`   | Robots file (links `sitemap.xml` if `SITE_URL` is set) |
| GET    | `/sitemap.xml`  | Sitemap XML                    |
| POST   | `/api/contact`  | JSON body: `name`, `email`, `subject`, `message` |

After validation, the contact form sends a real email via [Resend](https://resend.com) to `CONTACT_EMAIL` using the `RESEND_API_KEY` from `.env`. If `RESEND_API_KEY` is not set, submissions are only logged to the console (safe for local dev).

---

## Testing

The test suite uses [pytest](https://docs.pytest.org) and FastAPI's `TestClient` (built on `httpx`). Resend calls are mocked, so no real emails are sent and no API key is required.

```bash
pip install -r requirements-dev.txt
pytest -v
```

Coverage includes the landing page, `/health`, contact form success/validation/error responses, and rate limiting on `/api/contact`. Tests run automatically on every push and pull request via [GitHub Actions](.github/workflows/tests.yml).

---

## Customization

1. **Colors** — CSS variables in `static/css/styles.css` (`:root`)
2. **Fonts** — Google Fonts link in `templates/index.html` + `--font-*` in CSS
3. **Copy** — `templates/index.html` (demo brand: Luminary Studio)
4. **Validation messages** — `app/messages.py` (automatically synced to the frontend)
5. **SEO URL** — set `SITE_URL=https://yourdomain.com` when deploying

---

## Design decisions

- **One entry point** — `python main.py`; app logic stays in `app/`
- **No CORS middleware** — same-origin page + API; add CORS only if you split the frontend
- **`email-validator`** — used in `app/schemas.py` with user-facing messages from `app/messages.py`
- **Portfolio grid** — `grid-auto-rows` so implicit rows stay sized when cards are reordered

---

## License

MIT — free to use, modify, and adapt for client projects.
