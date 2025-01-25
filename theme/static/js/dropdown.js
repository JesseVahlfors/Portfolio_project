document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById("menu-button");
    const dropdownContent = document.getElementById("menu-content");

    dropdownButton.addEventListener('click', () => {
        dropdownContent.classList.toggle('hidden');

        const isExpanded = dropdownContent.classList.contains("hidden");
        dropdownButton.setAttribute("aria-expanded", !isExpanded);
    });

    const successMessage = document.querySelector('.success-message');
    if (successMessage) {
        // Scroll to the form when the success message appears
        document.getElementById('contact').scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    }
});