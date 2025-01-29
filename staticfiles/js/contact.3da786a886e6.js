
document.getElementById("contactForm").addEventListener('submit', async function(e){
    e.preventDefault(); 

    const form = e.target;
    const formData = new FormData(form);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;


    const response = await fetch(form.action, {
        method: "POST",
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
            'X-CSRFToken': csrfToken,
        }
    });

    const result = await response.json();
    const messageContainer = document.getElementById('message-container');
    messageContainer.style.display = 'block'; 
    messageContainer.textContent = '';

    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message', 'p-4', 'rounded-lg', 'mb-4');
    if (result.message) {
        messageDiv.textContent = result.message;
        if (response.ok) {
            messageDiv.textContent = result.message;
            messageDiv.style.backgroundColor = '#7CFC00';
            messageDiv.style.color = '#000080'; 
            form.reset();
        } else {
            messageDiv.textContent = result.message;
            messageDiv.style.backgroundColor = 'red';
            messageDiv.style.color = 'white';
        }
    }

    messageContainer.appendChild(messageDiv);
});

