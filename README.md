# Business Landing Page Template

A production-ready, fully responsive landing page template for service businesses — built with pure HTML/CSS/JS and a FastAPI backend. Ships with **Luminary Studio** as demo content (fictional interior design studio).

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat&logo=fastapi&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat&logo=python&logoColor=white)

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

Set env vars in your shell or use a process manager; `python main.py` reads them via `os.getenv`.

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
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app, routes, static/templates
│   ├── schemas.py       # ContactForm validation
│   └── messages.py      # Shared copy (validation + success text)
├── static/
│   ├── css/styles.css
│   └── js/app.js        # Reads validation rules from #app-config
├── templates/
│   └── index.html
├── main.py              # Single entry point (uvicorn)
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## API

| Method | Path            | Description                    |
|--------|-----------------|--------------------------------|
| GET    | `/`             | Landing page (Jinja2)          |
| GET    | `/health`       | `{"status": "ok"}`             |
| POST   | `/api/contact`  | JSON body: `name`, `email`, `subject`, `message` |

To send real email after validation, plug in [Resend](https://resend.com) or [SendGrid](https://sendgrid.com) inside the `contact` handler in `app/main.py`.

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
