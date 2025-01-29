document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById("menu-button");
    const dropdownContent = document.getElementById("menu-content");
    const menuItems = dropdownContent.querySelectorAll("a");

    dropdownButton.addEventListener('click', () => {
        dropdownContent.classList.toggle('hidden');

        const isExpanded = dropdownContent.classList.contains("hidden");
        dropdownButton.setAttribute("aria-expanded", !isExpanded);
    });

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            dropdownContent.classList.add('hidden');
            dropdownButton.setAttribute("aria-expanded", false);
        });
    });
});