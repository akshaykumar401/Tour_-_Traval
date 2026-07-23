const mobileMenuButton = document.getElementById("mobile-menu-button");
const mobileMenu = document.getElementById("mobile-menu");
const hamburgerIcon = document.getElementById("hamburger-icon");
const closeIcon = document.getElementById("close-icon");

// for mobile menu toggle....
if (mobileMenuButton && mobileMenu) {
  mobileMenuButton.addEventListener("click", function () {
    const isExpanded = mobileMenuButton.getAttribute("aria-expanded") === "true";

    mobileMenuButton.setAttribute("aria-expanded", !isExpanded);
    mobileMenu.classList.toggle("hidden");
    hamburgerIcon.classList.toggle("hidden");
    closeIcon.classList.toggle("hidden");
  });
}
