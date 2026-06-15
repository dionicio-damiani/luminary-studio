'use strict';

const appConfigEl = document.getElementById('app-config');
const VALIDATION = appConfigEl
  ? JSON.parse(appConfigEl.textContent).validation
  : {
      name: 'Name must be at least 2 characters.',
      email: 'Please enter a valid email address.',
      subject: 'Subject is required.',
      message: 'Message must be at least 10 characters.',
    };

// ── FADE-IN STAGGER VIA data-delay ───────────────────────
document.querySelectorAll('.fade-in[data-delay]').forEach(el => {
  el.style.animationDelay = `${el.dataset.delay}ms`;
});

// ── NAVBAR SCROLL BEHAVIOR ────────────────────────────────
const navbar = document.getElementById('navbar');
const navLinks = document.querySelectorAll('.nav-link');
const navSections = document.querySelectorAll(
  '#services, #portfolio, #process, #testimonials, #contact'
);

function onScroll() {
  navbar.classList.toggle('scrolled', window.scrollY > 60);

  let current = '';
  navSections.forEach(section => {
    const top = section.offsetTop - 120;
    if (window.scrollY >= top) current = section.id;
  });

  navLinks.forEach(link => {
    const href = link.getAttribute('href').replace('#', '');
    link.classList.toggle('active', href === current);
  });
}

window.addEventListener('scroll', onScroll, { passive: true });
onScroll();

// ── HERO SCROLL HINT FADE-OUT ─────────────────────────────
const scrollHint = document.querySelector('.hero-scroll-hint');
const SCROLL_HINT_FADE_DISTANCE = 150;

if (scrollHint) {
  let scrollHintTicking = false;

  function updateScrollHint() {
    const progress = Math.min(window.scrollY / SCROLL_HINT_FADE_DISTANCE, 1);
    scrollHint.style.opacity = String(1 - progress);
    scrollHint.classList.toggle('is-hidden', progress >= 1);
    scrollHintTicking = false;
  }

  window.addEventListener('scroll', () => {
    if (!scrollHintTicking) {
      requestAnimationFrame(updateScrollHint);
      scrollHintTicking = true;
    }
  }, { passive: true });

  updateScrollHint();
}

// ── MOBILE MENU ───────────────────────────────────────────
const hamburger = document.getElementById('hamburger');
const mobileMenu = document.getElementById('mobileMenu');
const mobileLinks = document.querySelectorAll('.mobile-link');

function toggleMenu(open) {
  hamburger.classList.toggle('open', open);
  hamburger.setAttribute('aria-expanded', open);
  mobileMenu.classList.toggle('open', open);
  mobileMenu.setAttribute('aria-hidden', !open);
}

hamburger.addEventListener('click', () => {
  toggleMenu(!hamburger.classList.contains('open'));
});

mobileLinks.forEach(link => {
  link.addEventListener('click', () => toggleMenu(false));
});

// ── SCROLL REVEAL ─────────────────────────────────────────
const revealItems = document.querySelectorAll('.reveal-item');

const revealObserver = new IntersectionObserver(
  entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const el = entry.target;
        const siblings = Array.from(el.parentElement.querySelectorAll('.reveal-item'));
        const index = siblings.indexOf(el);
        setTimeout(() => el.classList.add('visible'), index * 80);
        revealObserver.unobserve(el);
      }
    });
  },
  { threshold: 0.12, rootMargin: '0px 0px -40px 0px' }
);

revealItems.forEach(el => revealObserver.observe(el));

// ── PORTFOLIO LIGHTBOX ────────────────────────────────────
const portfolioCards = Array.from(document.querySelectorAll('.portfolio-card[data-project]'));
const lightbox       = document.getElementById('lightbox');
const lightboxImage  = document.getElementById('lightboxImage');
const lightboxCat    = document.getElementById('lightboxCategory');
const lightboxTitle  = document.getElementById('lightboxTitle');
const lightboxLoc    = document.getElementById('lightboxLocation');
const lightboxSize   = document.getElementById('lightboxSize');
const lightboxYear   = document.getElementById('lightboxYear');
const lightboxDesc   = document.getElementById('lightboxDesc');
const lightboxClose  = document.getElementById('lightboxClose');
const lightboxPrev   = document.getElementById('lightboxPrev');
const lightboxNext   = document.getElementById('lightboxNext');
const lightboxCta    = document.getElementById('lightboxCta');

let currentIndex   = -1;
let lastFocusedEl  = null;

function openLightbox(index) {
  const data = JSON.parse(portfolioCards[index].dataset.project);
  currentIndex = index;

  lightboxImage.style.backgroundImage = `url('${data.img}')`;
  lightboxCat.textContent   = data.category;
  lightboxTitle.textContent = data.title;
  lightboxLoc.textContent   = data.location;
  lightboxSize.textContent  = data.size;
  lightboxYear.textContent  = data.year;
  lightboxDesc.textContent  = data.desc;

  lightbox.classList.add('open');
  lightbox.setAttribute('aria-hidden', 'false');
  document.body.style.overflow = 'hidden';
  lightboxClose.focus();
}

function closeLightbox() {
  lightbox.classList.remove('open');
  lightbox.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
  if (lastFocusedEl) lastFocusedEl.focus();
}

function navigateLightbox(dir) {
  const len = portfolioCards.length;
  openLightbox((currentIndex + dir + len) % len);
}

portfolioCards.forEach((card, i) => {
  card.addEventListener('click', () => {
    lastFocusedEl = card;
    openLightbox(i);
  });
  card.addEventListener('keydown', e => {
    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      lastFocusedEl = card;
      openLightbox(i);
    }
  });
});

lightboxClose.addEventListener('click', closeLightbox);
lightboxPrev.addEventListener('click', () => navigateLightbox(-1));
lightboxNext.addEventListener('click', () => navigateLightbox(1));
lightboxCta.addEventListener('click', closeLightbox);

lightbox.addEventListener('click', e => {
  if (e.target === lightbox) closeLightbox();
});

// Focus trap inside lightbox
lightbox.addEventListener('keydown', e => {
  if (e.key !== 'Tab') return;
  const focusable = Array.from(
    lightbox.querySelectorAll('button:not([disabled]), a[href], [tabindex]:not([tabindex="-1"])')
  );
  const first = focusable[0];
  const last  = focusable[focusable.length - 1];
  if (e.shiftKey) {
    if (document.activeElement === first) { e.preventDefault(); last.focus(); }
  } else {
    if (document.activeElement === last)  { e.preventDefault(); first.focus(); }
  }
});

// ── GLOBAL KEYBOARD SHORTCUTS ─────────────────────────────
document.addEventListener('keydown', e => {
  if (lightbox.classList.contains('open')) {
    if (e.key === 'Escape')      closeLightbox();
    if (e.key === 'ArrowLeft')   navigateLightbox(-1);
    if (e.key === 'ArrowRight')  navigateLightbox(1);
  } else if (e.key === 'Escape' && hamburger.classList.contains('open')) {
    toggleMenu(false);
    hamburger.focus();
  }
});

// ── CONTACT FORM ──────────────────────────────────────────
const form       = document.getElementById('contactForm');
const submitBtn  = document.getElementById('submitBtn');
const formSuccess = document.getElementById('formSuccess');

const fields = {
  name:    { el: document.getElementById('name'),    errEl: document.getElementById('name-error') },
  email:   { el: document.getElementById('email'),   errEl: document.getElementById('email-error') },
  subject: { el: document.getElementById('subject'), errEl: document.getElementById('subject-error') },
  message: { el: document.getElementById('message'), errEl: document.getElementById('message-error') },
};

function setFieldError(key, message) {
  const { el, errEl } = fields[key];
  el.classList.toggle('error', !!message);
  errEl.textContent = message || '';
}

function clearErrors() {
  Object.keys(fields).forEach(key => setFieldError(key, ''));
  formSuccess.textContent = '';
  formSuccess.style.color = '';
}

function validateClient() {
  let valid = true;
  const name    = fields.name.el.value.trim();
  const email   = fields.email.el.value.trim().toLowerCase();
  const subject = fields.subject.el.value.trim();
  const message = fields.message.el.value.trim();

  if (name.length < 2) { setFieldError('name', VALIDATION.name); valid = false; }
  if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) { setFieldError('email', VALIDATION.email); valid = false; }
  if (!subject) { setFieldError('subject', VALIDATION.subject); valid = false; }
  if (message.length < 10) { setFieldError('message', VALIDATION.message); valid = false; }

  return valid;
}

function applyServerErrors(detail) {
  const errors = Array.isArray(detail) ? detail : [detail];
  errors.forEach(err => {
    const field = Array.isArray(err.loc) ? err.loc[err.loc.length - 1] : null;
    if (field && fields[field]) setFieldError(field, err.msg);
  });
}

form.addEventListener('submit', async e => {
  e.preventDefault();
  clearErrors();
  if (!validateClient()) return;

  submitBtn.disabled = true;
  submitBtn.classList.add('loading');

  const payload = {
    name:    fields.name.el.value.trim(),
    email:   fields.email.el.value.trim().toLowerCase(),
    subject: fields.subject.el.value.trim(),
    message: fields.message.el.value.trim(),
  };

  try {
    const res  = await fetch('/api/contact', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (res.ok && data.success) {
      formSuccess.textContent = data.message;
      form.reset();
    } else if (data.detail) {
      applyServerErrors(data.detail);
    } else {
      formSuccess.style.color = '#e07070';
      formSuccess.textContent = 'Something went wrong. Please try again.';
    }
  } catch {
    formSuccess.style.color = '#e07070';
    formSuccess.textContent = 'Network error. Please check your connection and try again.';
  } finally {
    submitBtn.disabled = false;
    submitBtn.classList.remove('loading');
  }
});

// ── SMOOTH SCROLL FOR ANCHOR LINKS ───────────────────────
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', e => {
    const target = document.querySelector(anchor.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});
