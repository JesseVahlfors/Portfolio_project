document.addEventListener('DOMContentLoaded', () => {
    const dropdownButton = document.getElementById("menu-button");
    const dropdownContent = document.getElementById("menu-content");

    dropdownButton.addEventListener('click', () => {
        dropdownContent.classList.toggle('hidden');
    });

});