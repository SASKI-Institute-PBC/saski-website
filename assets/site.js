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

const illustrationViewer = document.querySelector('[data-illustration-viewer]');
if (illustrationViewer) {
  const openers = [...document.querySelectorAll('[data-illustration-open]')];
  const stage = illustrationViewer.querySelector('[data-illustration-stage]');
  const canvas = illustrationViewer.querySelector('[data-illustration-canvas]');
  const image = illustrationViewer.querySelector('[data-illustration-image]');
  const title = illustrationViewer.querySelector('[data-illustration-title]');
  const caption = illustrationViewer.querySelector('[data-illustration-caption]');
  const original = illustrationViewer.querySelector('[data-illustration-original]');
  const zoomLevel = illustrationViewer.querySelector('[data-illustration-zoom-level]');
  let current = 0;
  let zoom = 1;
  let returnFocus = null;

  const sizeImage = () => {
    if (!image.naturalWidth || !stage.clientWidth || !stage.clientHeight) return;
    const gutter = 48;
    const fit = Math.min(
      (stage.clientWidth - gutter) / image.naturalWidth,
      (stage.clientHeight - gutter) / image.naturalHeight,
      1
    );
    const width = Math.round(image.naturalWidth * fit * zoom);
    const height = Math.round(image.naturalHeight * fit * zoom);
    canvas.style.width = `${width}px`;
    canvas.style.height = `${height}px`;
    canvas.style.marginLeft = width < stage.clientWidth - gutter ? `${Math.round((stage.clientWidth - width) / 2)}px` : '24px';
    canvas.style.marginTop = height < stage.clientHeight - gutter ? `${Math.round((stage.clientHeight - height) / 2)}px` : '24px';
    image.style.width = `${width}px`;
    image.style.height = `${height}px`;
    zoomLevel.textContent = `${Math.round(zoom * 100)}%`;
  };

  const setZoom = next => {
    zoom = Math.min(3, Math.max(1, next));
    sizeImage();
  };

  const showIllustration = index => {
    current = (index + openers.length) % openers.length;
    const opener = openers[current];
    zoom = 1;
    image.src = opener.dataset.src;
    image.alt = opener.querySelector('img').alt;
    title.textContent = opener.dataset.title;
    caption.textContent = opener.dataset.caption;
    original.href = opener.dataset.src;
    zoomLevel.textContent = '100%';
    stage.scrollTo(0, 0);
    requestAnimationFrame(sizeImage);
  };

  openers.forEach((opener, index) => {
    opener.addEventListener('click', () => {
      returnFocus = opener;
      showIllustration(index);
      illustrationViewer.showModal();
      requestAnimationFrame(sizeImage);
    });
  });
  image.addEventListener('load', sizeImage);
  illustrationViewer.querySelector('[data-illustration-previous]').addEventListener('click', () => showIllustration(current - 1));
  illustrationViewer.querySelector('[data-illustration-next]').addEventListener('click', () => showIllustration(current + 1));
  illustrationViewer.querySelector('[data-illustration-zoom-out]').addEventListener('click', () => setZoom(zoom - .25));
  illustrationViewer.querySelector('[data-illustration-zoom-in]').addEventListener('click', () => setZoom(zoom + .25));
  illustrationViewer.querySelector('[data-illustration-reset]').addEventListener('click', () => setZoom(1));
  illustrationViewer.querySelector('[data-illustration-close]').addEventListener('click', () => illustrationViewer.close());
  illustrationViewer.addEventListener('click', event => {
    if (event.target === illustrationViewer) illustrationViewer.close();
  });
  illustrationViewer.addEventListener('keydown', event => {
    if (event.key === 'ArrowLeft') showIllustration(current - 1);
    if (event.key === 'ArrowRight') showIllustration(current + 1);
    if (event.key === '+' || event.key === '=') setZoom(zoom + .25);
    if (event.key === '-') setZoom(zoom - .25);
  });
  illustrationViewer.addEventListener('close', () => returnFocus?.focus());
  window.addEventListener('resize', sizeImage);
}
