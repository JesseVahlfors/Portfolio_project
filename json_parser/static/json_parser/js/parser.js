const form = document.getElementById('json-form');
const result = document.getElementById('result');

form.addEventListener('submit', async (e) => {
    e.preventDefault();

    const formData = new FormData(form);
    result.classList.add('hidden');
    result.textContent = "Parsing...";

    try  {
        const response = await fetch(form.action, {
            method: 'POST',
            headers:  {
                'X-CSFRFToken': csrfToken,
            },
            body: formData,
        });

        const data = await response.json();

        if (data.success) {
            result.textContent = JSON.stringify(data.parsed, null, 2);
            result.classList.remove('hidden', 'bg-red-100');
            result.classList.add('bg-gray-100');
        } else {
            result.textContent = "Error: " + data.error;
            result.classList.remove('hidden', 'bg-gray-100');
            result.classList.add('bg-red-100');
        }
    } catch (error) {
        result.textContent = "Unexpected error occurred ";
        result.classList.remove('hidden');
        result.classList.add('bg-red-100');
    }
});