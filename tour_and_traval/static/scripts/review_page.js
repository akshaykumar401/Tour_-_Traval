// Global functions
function showSuccessToast() {
  const toast = document.getElementById("toast-success");
  toast.classList.remove("translate-x-80", "opacity-0");
  toast.classList.add("translate-x-0", "opacity-100");

  // Clear form
  document.getElementById("review-form").reset();
  document.getElementById("rating-input").value = "0";

  // Trigger hover-out to reset stars to empty
  const stars = document.querySelectorAll(".star-btn");
  stars.forEach((s) => {
    s.classList.remove("text-amber-400");
    s.classList.add("text-slate-200");
  });

  setTimeout(() => {
    toast.classList.add("translate-x-80", "opacity-0");
    toast.classList.remove("translate-x-0", "opacity-100");
  }, 4000);
}

document.addEventListener("DOMContentLoaded", () => {
  // 1. Star Rating Interactive Logic
  const stars = document.querySelectorAll(".star-btn");
  const ratingInput = document.getElementById("rating-input");

  stars.forEach((star) => {
    // Hover In
    star.addEventListener("mouseenter", () => {
      const value = parseInt(star.getAttribute("data-value"));
      highlightStars(value);
    });

    // Hover Out
    star.addEventListener("mouseleave", () => {
      const currentValue = parseInt(ratingInput.value) || 0;
      highlightStars(currentValue);
    });

    // Click
    star.addEventListener("click", () => {
      const value = parseInt(star.getAttribute("data-value"));
      ratingInput.value = value;
      highlightStars(value);
    });
  });

  function highlightStars(count) {
    stars.forEach((star) => {
      const value = parseInt(star.getAttribute("data-value"));
      if (value <= count) {
        star.classList.remove("text-slate-200");
        star.classList.add("text-amber-400");
      } else {
        star.classList.remove("text-amber-400");
        star.classList.add("text-slate-200");
      }
    });
  }
});
