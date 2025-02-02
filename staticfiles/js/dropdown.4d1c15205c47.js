document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById("menu-button");
    const closeButton = document.getElementById("close-button");
    const dropdownContent = document.getElementById("menu-content");
    const menuItems = dropdownContent.querySelectorAll("a");

    const toggleDropdown = () => {
        dropdownContent.classList.toggle('hidden');
        dropdownButton.classList.toggle('hidden');
        closeButton.classList.toggle('hidden');

        const isExpanded = dropdownContent.classList.contains("hidden");
        dropdownButton.setAttribute("aria-expanded", !isExpanded);
        closeButton.setAttribute("aria-expanded", isExpanded);
    };

    dropdownButton.addEventListener('click', toggleDropdown);
    closeButton.addEventListener('click', toggleDropdown);

    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            dropdownContent.classList.add('hidden');
            dropdownButton.setAttribute("aria-expanded", false);
            closeButton.classList.add('hidden');
            dropdownButton.setAttribute("aria-expanded", false);
        });
    });
});