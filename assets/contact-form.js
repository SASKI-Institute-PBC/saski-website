document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('[data-contact-form]');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const status = document.querySelector('[data-contact-status]');
    const button = form.querySelector('button[type="submit"]');
    const originalLabel = button.textContent;
    const body = new URLSearchParams();
    new FormData(form).forEach((value, key) => body.append(key, value));

    button.disabled = true;
    button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    if (status) status.textContent = 'Sending your message…';

    try {
      await fetch(form.action, {
        method: 'POST',
        body,
        mode: 'no-cors',
        redirect: 'follow',
      });
      form.reset();
      if (status) status.textContent = 'Thank you. Your message has been sent to SASKI.';
    } catch (error) {
      if (status) status.textContent = 'The message could not be sent. Please email info@saski.io.';
    } finally {
      button.disabled = false;
      button.textContent = originalLabel;
      form.removeAttribute('aria-busy');
    }
  });
});
