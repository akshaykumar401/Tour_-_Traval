document.addEventListener('DOMContentLoaded', () => {
  const filterBtn = document.getElementById('filter-btn');
  const filterDropdown = document.getElementById('filter-dropdown');
  const sortBtn = document.getElementById('sort-btn');
  const sortDropdown = document.getElementById('sort-dropdown');
  const sortLabel = document.getElementById('sort-label');
  
  const priceRange = document.getElementById('price-range');
  const priceVal = document.getElementById('price-val');
  const clearFiltersBtn = document.getElementById('clear-filters-btn');
  const applyFiltersBtn = document.getElementById('apply-filters-btn');
  
  const packagesGrid = document.getElementById('packages-grid');
  const cards = Array.from(packagesGrid.querySelectorAll('.package-card'));
  
  // Store original order for 'Recommended' sorting
  const originalOrder = [...cards];

  // Helper to format currency
  const formatCurrency = (val) => {
    return '₹' + parseInt(val).toLocaleString('en-IN');
  };

  // Toggle dropdowns
  filterBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    filterDropdown.classList.toggle('hidden');
    sortDropdown.classList.add('hidden');
  });

  sortBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    sortDropdown.classList.toggle('hidden');
    filterDropdown.classList.add('hidden');
  });

  // Close dropdowns when clicking outside
  document.addEventListener('click', (e) => {
    if (!filterDropdown.contains(e.target) && e.target !== filterBtn && !filterBtn.contains(e.target)) {
      filterDropdown.classList.add('hidden');
    }
    if (!sortDropdown.contains(e.target) && e.target !== sortBtn && !sortBtn.contains(e.target)) {
      sortDropdown.classList.add('hidden');
    }
  });

  // Dynamic price slider update
  priceRange.addEventListener('input', () => {
    priceVal.textContent = formatCurrency(priceRange.value);
  });

  // Clear filters
  clearFiltersBtn.addEventListener('click', () => {
    // Uncheck categories
    document.querySelectorAll('input[name="category"]').forEach(cb => cb.checked = false);
    // Uncheck durations
    document.querySelectorAll('input[name="duration"]').forEach(cb => cb.checked = false);
    // Reset price
    priceRange.value = 50000;
    priceVal.textContent = formatCurrency(50000);
    
    applyFilters();
  });

  // Apply filters
  const applyFilters = () => {
    const checkedCategories = Array.from(document.querySelectorAll('input[name="category"]:checked')).map(cb => cb.value);
    const checkedDurations = Array.from(document.querySelectorAll('input[name="duration"]:checked')).map(cb => cb.value);
    const maxPrice = parseInt(priceRange.value);

    let visibleCount = 0;

    cards.forEach(card => {
      const category = card.dataset.category;
      const price = parseInt(card.dataset.price);
      const duration = parseInt(card.dataset.duration);

      let matchCategory = checkedCategories.length === 0 || checkedCategories.includes(category);
      let matchPrice = price <= maxPrice;
      
      let matchDuration = checkedDurations.length === 0;
      if (checkedDurations.length > 0) {
        checkedDurations.forEach(d => {
          if (d === 'short' && duration >= 3 && duration <= 5) matchDuration = true;
          if (d === 'medium' && duration >= 6 && duration <= 8) matchDuration = true;
        });
      }

      if (matchCategory && matchPrice && matchDuration) {
        card.style.display = '';
        visibleCount++;
      } else {
        card.style.display = 'none';
      }
    });

    // Check if no results found
    let noResultsMsg = document.getElementById('no-results-message');
    if (visibleCount === 0) {
      if (!noResultsMsg) {
        noResultsMsg = document.createElement('div');
        noResultsMsg.id = 'no-results-message';
        noResultsMsg.className = 'col-span-full py-16 text-center space-y-3';
        noResultsMsg.innerHTML = `
          <i class="ri-search-line text-4xl text-slate-350"></i>
          <h4 class="text-lg font-bold text-slate-800">No packages found</h4>
          <p class="text-sm text-slate-500 font-light">Try adjusting your filters or clearing them to start over.</p>
        `;
        packagesGrid.appendChild(noResultsMsg);
      }
    } else {
      if (noResultsMsg) {
        noResultsMsg.remove();
      }
    }
    
    filterDropdown.classList.add('hidden');
  };

  applyFiltersBtn.addEventListener('click', applyFilters);

  // Sorting
  const sortOptions = document.querySelectorAll('.sort-option');
  sortOptions.forEach(option => {
    option.addEventListener('click', () => {
      const sortBy = option.dataset.sort;
      
      // Update active option styles
      sortOptions.forEach(opt => {
        opt.classList.remove('text-[#8c5a24]', 'bg-slate-50', 'font-bold');
        opt.classList.add('text-slate-600');
        const checkIcon = opt.querySelector('.ri-check-line');
        if (checkIcon) checkIcon.remove();
      });

      option.classList.add('text-[#8c5a24]', 'bg-slate-50', 'font-bold');
      option.classList.remove('text-slate-600');
      
      const checkIcon = document.createElement('i');
      checkIcon.className = 'ri-check-line text-[#8c5a24]';
      option.appendChild(checkIcon);

      // Update button label
      const text = option.querySelector('span').textContent;
      sortLabel.textContent = `Sort By: ${text}`;

      // Sort logic
      let sortedCards = [];
      if (sortBy === 'recommended') {
        sortedCards = [...originalOrder];
      } else if (sortBy === 'price-low') {
        sortedCards = [...cards].sort((a, b) => parseInt(a.dataset.price) - parseInt(b.dataset.price));
      } else if (sortBy === 'price-high') {
        sortedCards = [...cards].sort((a, b) => parseInt(b.dataset.price) - parseInt(a.dataset.price));
      } else if (sortBy === 'rating') {
        sortedCards = [...cards].sort((a, b) => parseFloat(b.dataset.rating) - parseFloat(a.dataset.rating));
      } else if (sortBy === 'duration') {
        sortedCards = [...cards].sort((a, b) => parseInt(a.dataset.duration) - parseInt(b.dataset.duration));
      }

      // Re-append sorted cards
      sortedCards.forEach(card => packagesGrid.appendChild(card));
      
      // Keep no results message at the bottom if present
      const noResultsMsg = document.getElementById('no-results-message');
      if (noResultsMsg) packagesGrid.appendChild(noResultsMsg);

      sortDropdown.classList.add('hidden');
    });
  });
});
