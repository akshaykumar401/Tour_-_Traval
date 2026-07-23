document.addEventListener("DOMContentLoaded", () => {
  const pills = document.querySelectorAll(".filter-pill");
  const items = document.querySelectorAll(".gallery-item");
  const emptyState = document.getElementById("gallery-empty-state");

  pills.forEach((pill) => {
    pill.addEventListener("click", () => {
      const filter = pill.dataset.filter;

      // Update active styles
      pills.forEach((p) => {
        p.className =
          "filter-pill bg-white text-slate-600 border border-slate-200 hover:border-slate-300 hover:text-slate-900 text-xs sm:text-sm font-semibold px-5 py-2.5 rounded-full transition-all duration-200 cursor-pointer shadow-xs";
      });
      pill.className =
        "filter-pill bg-[#051120] text-white text-xs sm:text-sm font-semibold px-5 py-2.5 rounded-full transition-all duration-200 cursor-pointer shadow-xs hover:shadow-md";

      // Apply filter
      let visibleCount = 0;
      items.forEach((item) => {
        const category = item.dataset.category;
        if (filter === "all" || category === filter) {
          item.style.display = "";
          visibleCount++;
        } else {
          item.style.display = "none";
        }
      });

      // Show empty state if needed
      if (visibleCount === 0) {
        emptyState.classList.remove("hidden");
      } else {
        emptyState.classList.add("hidden");
      }
    });
  });
});
