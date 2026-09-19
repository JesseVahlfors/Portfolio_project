// Dropdown menu functionality

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

// Allow HTMX to display contact form error responses (400/500/etc.)
// by swapping the returned form HTML into the contact form container.

document.body.addEventListener("htmx:beforeSwap", (event) => {
  const target = event.detail.target;

  if (target?.id === "contact-form-slot" && event.detail.xhr.status >= 400) {
    event.detail.shouldSwap = true;
    event.detail.isError = false;
  }
});

// Re-render reCAPTCHA after HTMX replaces the contact form.
document.body.addEventListener("htmx:afterSwap", (event) => {
  if (event.detail.target?.id === "contact-form-slot") {
    const recaptcha = event.detail.target.querySelector(".g-recaptcha");

    if (recaptcha && window.grecaptcha) {
      grecaptcha.render(recaptcha);
    }
  }
});
