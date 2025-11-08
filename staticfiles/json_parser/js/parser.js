const form = document.getElementById('json-form');
const result = document.getElementById('result');
const fileInput = document.getElementById('json-file');
const textArea = document.getElementById('json-input');
const inputWarning = document.getElementById('input-warning')

// form submission 

form.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    result.classList.add('hidden');
    result.textContent = "Parsing...";
    
    const formData = new FormData();
    if (fileInput.files.length > 0) {
        formData.append('json_file', fileInput.files[0]);
    } else {
        formData.append('json_input', textArea.value);
    }


    try  {
        const response = await fetch(form.action, {
            method: 'POST',
            headers:  {
                'X-CSRFToken': csrfToken,
            },
            body: formData,
        });

        const responseText = await response.text();
        let data;
        try {
            data = JSON.parse(responseText);
        } catch (parseError) {
            throw new Error("Invalid JSON response from server:\n" + responseText);
        }

        if (data.status === 'success') {
            const codeBlock = document.getElementById('result');
            codeBlock.textContent = JSON.stringify(data.data, null, 2);
            result.classList.remove('hidden');
            Prism.highlightElement(codeBlock);
        } else {
            result.textContent = (data.message || "Unknown error");
            result.classList.remove('hidden', 'bg-gray-100');
            result.classList.add('bg-red-100');
        }
    } catch (error) {
        result.textContent = `Invalid JSON: ${error.message || error}`;
        result.classList.remove('hidden');
        result.classList.add('bg-red-100');
    }
});

// file input handling

document.addEventListener('DOMContentLoaded', () => {
    const fileInput = document.getElementById('json-file');
    const fileNameDisplay = document.getElementById('file-name-display');
    const clearButton = document.getElementById('clear-button');

    fileInput.addEventListener('change', (event) => {
        const fileName = event.target.files[0]?.name || 'No file selected';
        fileNameDisplay.textContent = fileName;
        inputWarning.classList.remove('hidden')
        textArea.classList.add('hidden')
    });

    clearButton.addEventListener('click', () => {
        fileInput.value = '';
        fileNameDisplay.textContent = 'No file selected';
        inputWarning.classList.add('hidden')
        textArea.classList.remove('hidden')
    });
});

// dropdown option handling

document.addEventListener('DOMContentLoaded', () => {
    const dropdown = document.getElementById('json-dropdown');
    if (fileInput.files.length > 0) {

    } else {
        dropdown.addEventListener('change', (event) => {
            textArea.value = event.target.value || '';
        }); 
    }
});
