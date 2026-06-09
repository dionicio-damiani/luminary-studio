import json
import logging
import os
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.util import get_remote_address

from app.messages import CONTACT_SUCCESS, VALIDATION
from app.schemas import ContactForm

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent.parent
SITE_URL = os.getenv("SITE_URL", "").rstrip("/")
RESEND_API_KEY = os.getenv("RESEND_API_KEY", "")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL", "hello@luminarystudio.com")

limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title="Business Landing Page",
    description="Reusable service-business landing template (demo: Luminary Studio).",
    version="1.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.middleware("http")
async def security_headers(request: Request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "SAMEORIGIN"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "camera=(), microphone=(), geolocation=()"
    return response


@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    return templates.TemplateResponse(
        request, "404.html", {"year": datetime.now().year}, status_code=404
    )


@app.exception_handler(500)
async def server_error_handler(request: Request, exc):
    logger.error("Internal server error: %s", exc)
    return JSONResponse(status_code=500, content={"success": False, "message": "Internal server error."})


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/robots.txt", response_class=PlainTextResponse)
async def robots():
    lines = ["User-agent: *", "Allow: /"]
    if SITE_URL:
        lines.append(f"Sitemap: {SITE_URL}/sitemap.xml")
    return "\n".join(lines)


@app.get("/sitemap.xml")
async def sitemap():
    base = SITE_URL or "http://localhost:8000"
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>{base}/</loc>
    <changefreq>monthly</changefreq>
    <priority>1.0</priority>
  </url>
</urlset>"""
    return HTMLResponse(xml, media_type="application/xml")


def _app_config_json() -> str:
    return json.dumps({"validation": VALIDATION})


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "year": datetime.now().year,
            "site_url": SITE_URL,
            "app_config_json": _app_config_json(),
        },
    )


async def _send_email(form: ContactForm) -> None:
    if not RESEND_API_KEY:
        logger.info("Contact form [no email key] — %s <%s>: %s", form.name, form.email, form.subject)
        return
    try:
        import resend  # installed via requirements.txt
        resend.api_key = RESEND_API_KEY
        resend.Emails.send({
            "from": "Luminary Studio <onboarding@resend.dev>",
            "to": RECIPIENT_EMAIL,
            "reply_to": form.email,
            "subject": f"New inquiry from {form.name}: {form.subject}",
            "html": (
                f"<h2 style='font-family:sans-serif'>New Contact Form Submission</h2>"
                f"<p><strong>Name:</strong> {form.name}</p>"
                f"<p><strong>Email:</strong> {form.email}</p>"
                f"<p><strong>Subject:</strong> {form.subject}</p>"
                f"<hr>"
                f"<p style='white-space:pre-wrap'>{form.message}</p>"
            ),
        })
        logger.info("Email sent for contact from %s <%s>", form.name, form.email)
    except Exception as exc:
        logger.error("Email send failed: %s", exc)


@app.post("/api/contact")
@limiter.limit("5/minute")
async def contact(request: Request, form: ContactForm):
    await _send_email(form)
    return JSONResponse(
        status_code=200,
        content={"success": True, "message": CONTACT_SUCCESS.format(name=form.name)},
    )
