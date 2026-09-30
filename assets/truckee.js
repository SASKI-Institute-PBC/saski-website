document.addEventListener('DOMContentLoaded', () => {
  const form = document.querySelector('[data-truckee-form]');
  if (!form) return;

  form.addEventListener('submit', (event) => {
    event.preventDefault();
    if (!form.reportValidity()) return;

    const values = Object.fromEntries(new FormData(form));
    const subject = `Truckee AI walkthrough request — ${values.business || values.name}`;
    const body = [
      `Name: ${values.name}`,
      `Business: ${values.business}`,
      `Phone: ${values.phone}`,
      `Email: ${values.email}`,
      '',
      'What takes up too much time:',
      values.challenge || 'Not provided',
    ].join('\n');

    const status = document.querySelector('[data-truckee-status]');
    if (status) status.textContent = 'Your email app should open with your request ready to send.';
    window.location.href = `mailto:info@saski.io?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
  });
});
