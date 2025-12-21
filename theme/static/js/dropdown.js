document.addEventListener("DOMContentLoaded", () => {
  const menuButton = document.getElementById("menu-button");
  const menuContent = document.getElementById("menu-content");

  if (!menuButton || !menuContent) return;

  const openMenu = () => {
    menuContent.classList.remove("hidden");
    menuButton.setAttribute("aria-expanded", "true");
  };

  const closeMenu = () => {
    menuContent.classList.add("hidden");
    menuButton.setAttribute("aria-expanded", "false");
  };

  const toggleMenu = (e) => {
    e.stopPropagation();
    menuContent.classList.contains("hidden") ? openMenu() : closeMenu();
  };

  // Toggle on button click
  menuButton.addEventListener("click", toggleMenu);

  // Close when clicking a menu item
  menuContent.querySelectorAll("a").forEach((link) => {
    link.addEventListener("click", closeMenu);
  });

  // Close when clicking outside
  document.addEventListener("click", (e) => {
    if (!menuContent.contains(e.target) && !menuButton.contains(e.target)) {
      closeMenu();
    }
  });

  // Close on Escape key
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") {
      closeMenu();
    }
  });
});
