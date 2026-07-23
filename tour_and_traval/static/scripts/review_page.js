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

  const reviewsGrid = document.getElementById("reviews-grid");
  const reviewsLoader = document.getElementById("reviews-loader");
  let isLoadingReviews = false;

  async function loadMoreReviews() {
    const nextPage = reviewsLoader?.dataset.nextPage;
    if (!nextPage || isLoadingReviews) return;

    isLoadingReviews = true;
    reviewsLoader.innerHTML = '<span class="text-sm text-slate-500">Loading more reviews…</span>';

    try {
      const url = new URL(reviewsLoader.dataset.url, window.location.origin);
      url.searchParams.set("page", nextPage);
      const response = await fetch(url, { headers: { "X-Requested-With": "XMLHttpRequest" } });
      if (!response.ok) throw new Error("Could not load reviews");

      const data = await response.json();
      reviewsGrid.insertAdjacentHTML("beforeend", data.html);
      reviewsLoader.dataset.nextPage = data.next_page || "";
      reviewsLoader.innerHTML = data.has_next ? '<span class="text-sm text-slate-500">Loading more reviews…</span>' : "";
    } catch (error) {
      reviewsLoader.innerHTML = '<span class="text-sm text-red-600">Unable to load more reviews.</span>';
    } finally {
      isLoadingReviews = false;
    }
  }

  if (reviewsLoader && reviewsLoader.dataset.nextPage && "IntersectionObserver" in window) {
    const observer = new IntersectionObserver((entries) => {
      if (entries[0].isIntersecting) loadMoreReviews();
    }, { rootMargin: "200px" });
    observer.observe(reviewsLoader);
  }
});
