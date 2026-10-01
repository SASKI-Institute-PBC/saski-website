document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('[data-truckee-form]');
  if (!form) return;

  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const status = document.querySelector('[data-truckee-status]');
    const button = form.querySelector('button[type="submit"]');
    const originalLabel = button.textContent;
    const body = new URLSearchParams();
    new FormData(form).forEach((value, key) => body.append(key, value));

    button.disabled = true;
    button.textContent = 'Sending…';
    form.setAttribute('aria-busy', 'true');
    if (status) status.textContent = 'Sending your request…';

    try {
      await fetch(form.action, {
        method: 'POST',
        body,
        mode: 'no-cors',
        redirect: 'follow',
      });
      form.reset();
      if (status) status.textContent = 'Thank you. Your request has been sent to SASKI.';
    } catch (error) {
      if (status) status.textContent = 'The message could not be sent. Please email info@saski.io or call 707.287.4544.';
    } finally {
      button.disabled = false;
      button.textContent = originalLabel;
      form.removeAttribute('aria-busy');
    }
  });
});
