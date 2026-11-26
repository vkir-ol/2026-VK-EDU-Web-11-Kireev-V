document.addEventListener('submit', async (event) => {
    const form = event.target;
    if (!form.matches('form.pk-vote')) return;

    event.preventDefault();
    if (!event.submitter || form.dataset.sending) return;

    const data = new FormData(form);
    data.set('value', event.submitter.value);
    form.dataset.sending = 'true';

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: data,
        });

        if (response.status === 403) {
            alert('Не удалось проверить CSRF-токен. Обновите страницу и попробуйте снова.');
            return;
        }

        const result = await response.json();
        if (!response.ok) {
            alert(result.error || 'Не удалось сохранить голос.');
            return;
        }

        form.querySelector('.pk-vote-count').textContent = result.rating;
    } catch {
        alert('Не удалось получить ответ сервера. Обновите страницу и проверьте рейтинг.');
    } finally {
        delete form.dataset.sending;
    }
});