document.addEventListener('submit', async (event) => {
    const form = event.target;
    if (!form.matches('form.js-correct-answer')) return;

    event.preventDefault();
    const button = form.querySelector('button');
    if (button.disabled) return;
    button.disabled = true;

    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
        });

        const contentType = response.headers.get('content-type') || '';
        if (!contentType.includes('application/json')) {
            alert(response.status === 403
                ? 'Проверка CSRF не прошла. Обновите страницу и попробуйте снова.'
                : 'Сервер вернул неожиданный ответ. Обновите страницу.');
            return;
        }

        const result = await response.json();
        if (!response.ok) {
            alert(result.error || 'Не удалось выбрать ответ.');
            return;
        }

        history.replaceState(null, '', result.url);
        window.location.reload();
    } catch {
        alert('Не удалось получить ответ сервера. Обновите страницу и проверьте отметку.');
    } finally {
        button.disabled = false;
    }
});