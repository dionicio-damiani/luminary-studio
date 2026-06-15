'use strict';

// Shared navbar behavior for secondary pages (e.g. Privacy, Terms):
// sticky background on scroll + mobile hamburger menu.

const navbar = document.getElementById('navbar');

window.addEventListener('scroll', () => {
  navbar.classList.toggle('scrolled', window.scrollY > 60);
}, { passive: true });

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

document.addEventListener('keydown', e => {
  if (e.key === 'Escape' && hamburger.classList.contains('open')) {
    toggleMenu(false);
    hamburger.focus();
  }
});
