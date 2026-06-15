"""Shared user-facing copy for form validation (API + frontend via template)."""

VALIDATION = {
    "name": "Name must be at least 2 characters.",
    "email": "Please enter a valid email address.",
    "subject": "Subject is required.",
    "message": "Message must be at least 10 characters.",
}

CONTACT_SUCCESS = "Thank you, {name}. We'll get back to you within 24 hours."
CONTACT_ERROR = "Sorry, we couldn't send your message right now. Please try again later."
