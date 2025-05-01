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
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        const data = await response.json();

        if (data.status === 'success') {
            result.textContent = JSON.stringify(data.data, null, 2);
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

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('json-file');
    const fileNameDisplay = document.getElementById('file-name-display');
    const clearButton = document.getElementById('clear-button');

    fileInput.addEventListener('change', (event) => {
        const fileName = event.target.files[0]?.name || 'No file selected';
        fileNameDisplay.textContent = fileName;
    });

    clearButton.addEventListener('click', () => {
        fileInput.value = '';
        fileNameDisplay.textContent = 'No file selected';
    });
});