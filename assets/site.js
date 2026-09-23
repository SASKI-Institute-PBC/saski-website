'use strict';
document.documentElement.classList.add('js');
const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('#navigation');
if (toggle && nav) {
  toggle.hidden = false;
  toggle.addEventListener('click', () => {
    const open = toggle.getAttribute('aria-expanded') !== 'true';
    toggle.setAttribute('aria-expanded', String(open));
    nav.classList.toggle('open', open);
    toggle.textContent = open ? 'Close' : 'Menu';
  });
  document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && toggle.getAttribute('aria-expanded') === 'true') {
      toggle.click(); toggle.focus();
    }
  });
}
const form = document.querySelector('#calculator');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    if (!form.reportValidity()) return;
    const [turns, current, proposed, price] = ['turns','legacy','lean','price'].map(id => Number(document.getElementById(id).value));
    const reduction = turns * (current - proposed);
    const monthly = reduction * price / 1000000;
    const money = n => n.toLocaleString('en-US', { style:'currency',currency:'USD' });
    document.getElementById('monthly').textContent = money(monthly);
    document.getElementById('annual').textContent = money(monthly * 12);
    document.getElementById('tokens').textContent = reduction.toLocaleString('en-US');
    document.getElementById('percent').textContent = current > 0 ? ((current-proposed)/current*100).toFixed(1)+'%' : 'Not applicable';
    document.getElementById('calc-note').textContent = proposed > current ? 'Negative savings: the proposed prompt increases repeated input-token cost.' : 'This estimate covers repeated input tokens only.';
  });
}

const consent = document.querySelector('[data-analytics-consent]');
const manageConsent = document.querySelector('[data-manage-consent]');
const consentKey = 'saski-analytics-consent';
let analyticsLoaded = false;
const loadAnalytics = () => {
  if (analyticsLoaded || !window.SASKI_GA_ID) return;
  analyticsLoaded = true;
  window.dataLayer = window.dataLayer || [];
  window.gtag = function(){ window.dataLayer.push(arguments); };
  window.gtag('js', new Date());
  window.gtag('config', window.SASKI_GA_ID, {
    allow_google_signals: false,
    allow_ad_personalization_signals: false
  });
  const script = document.createElement('script');
  script.async = true;
  script.src = `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(window.SASKI_GA_ID)}`;
  document.head.appendChild(script);
};
if (consent) {
  const choice = localStorage.getItem(consentKey);
  if (choice === 'granted') loadAnalytics();
  if (!choice) consent.hidden = false;
  consent.querySelectorAll('[data-consent]').forEach(button => {
    button.addEventListener('click', () => {
      const nextChoice = button.dataset.consent;
      localStorage.setItem(consentKey, nextChoice);
      consent.hidden = true;
      if (nextChoice === 'granted') loadAnalytics();
    });
  });
  manageConsent?.addEventListener('click', () => {
    consent.hidden = false;
    consent.querySelector('[data-consent="declined"]').focus();
  });
}
