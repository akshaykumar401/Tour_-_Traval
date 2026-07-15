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
    console.log(`Star button event listeners attached. ${star.getAttribute("data-value")}`);
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
