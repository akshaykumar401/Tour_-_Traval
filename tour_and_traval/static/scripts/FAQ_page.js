document.addEventListener("DOMContentLoaded", () => {
  // --- ACCORDION FUNCTIONALITY ---
  const faqItems = document.querySelectorAll(".faq-item");
  
  faqItems.forEach(item => {
    const toggle = item.querySelector(".faq-toggle");
    const container = item.querySelector(".faq-answer-container");
    const icon = item.querySelector(".ri-arrow-down-s-line");
    
    toggle.addEventListener("click", () => {
      const isOpen = container.style.maxHeight && container.style.maxHeight !== "0px";
      
      // Close all other accordions (optional, but makes UI very clean)
      // If we want multiple open at once, we can comment this out.
      document.querySelectorAll(".faq-answer-container").forEach(c => {
        c.style.maxHeight = null;
        c.parentElement.querySelector(".ri-arrow-down-s-line").style.transform = "rotate(0deg)";
        c.parentElement.classList.remove("border-slate-350");
      });
      
      if (!isOpen) {
        // Open this accordion
        container.style.maxHeight = container.scrollHeight + "px";
        icon.style.transform = "rotate(180deg)";
        item.classList.add("border-slate-350");
      } else {
        // Close this accordion
        container.style.maxHeight = "0px";
        icon.style.transform = "rotate(0deg)";
        item.classList.remove("border-slate-350");
      }
    });
  });

  // --- CATEGORY SIDEBAR SWITCHING AND SCROLLING ---
  const categoryBtns = document.querySelectorAll(".category-btn");
  const faqSections = document.querySelectorAll(".faq-section");
  let isScrolling = false;

  // Add scroll margins to sections to account for sticky header
  faqSections.forEach(section => {
    section.style.scrollMarginTop = "100px";
  });

  categoryBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      const targetCategory = btn.getAttribute("data-category");
      const targetSection = document.getElementById(`section-${targetCategory}`);
      
      if (targetSection) {
        isScrolling = true;
        
        // Update active class in sidebar
        categoryBtns.forEach(b => {
          b.classList.remove("active", "bg-[#0f2440]", "text-white", "shadow-xs");
          b.classList.add("text-slate-600", "hover:bg-slate-100", "hover:text-slate-900");
        });
        
        btn.classList.add("active", "bg-[#0f2440]", "text-white", "shadow-xs");
        btn.classList.remove("text-slate-600", "hover:bg-slate-100", "hover:text-slate-900");
        
        // Clear search input if active to show all categories
        const searchInput = document.getElementById("faq-search");
        if (searchInput.value.trim() !== "") {
          searchInput.value = "";
          handleSearch("");
        }

        // Scroll smoothly
        targetSection.scrollIntoView({ behavior: "smooth" });
        
        // Reset scrolling flag after animation
        setTimeout(() => {
          isScrolling = false;
        }, 800);
      }
    });
  });

  // Highlight category based on scroll position
  window.addEventListener("scroll", () => {
    if (isScrolling) return;
    
    let currentSectionId = "";
    const scrollPos = window.scrollY + 120; // offset

    faqSections.forEach(section => {
      if (window.scrollY === 0) {
        currentSectionId = "booking";
        return;
      }
      const sectionTop = section.offsetTop;
      const sectionHeight = section.offsetHeight;
      if (scrollPos >= sectionTop && scrollPos < sectionTop + sectionHeight) {
        currentSectionId = section.id.replace("section-", "");
      }
    });

    if (currentSectionId) {
      categoryBtns.forEach(btn => {
        const category = btn.getAttribute("data-category");
        if (category === currentSectionId) {
          btn.classList.add("active", "bg-[#0f2440]", "text-white", "shadow-xs");
          btn.classList.remove("text-slate-600", "hover:bg-slate-100", "hover:text-slate-900");
        } else {
          btn.classList.remove("active", "bg-[#0f2440]", "text-white", "shadow-xs");
          btn.classList.add("text-slate-600", "hover:bg-slate-100", "hover:text-slate-900");
        }
      });
    }
  });

  // --- SEARCH FILTERING ---
  const searchInput = document.getElementById("faq-search");
  const clearSearchBtn = document.getElementById("clear-search-btn");
  const noResultsDiv = document.getElementById("no-results");
  
  searchInput.addEventListener("input", (e) => {
    const query = e.target.value.toLowerCase().trim();
    handleSearch(query);
  });

  clearSearchBtn.addEventListener("click", () => {
    searchInput.value = "";
    handleSearch("");
    searchInput.focus();
  });

  function handleSearch(query) {
    if (query === "") {
      clearSearchBtn.classList.add("hidden");
    } else {
      clearSearchBtn.classList.remove("hidden");
    }

    let overallMatches = 0;

    faqSections.forEach(section => {
      const items = section.querySelectorAll(".faq-item");
      let sectionMatches = 0;

      items.forEach(item => {
        const question = item.querySelector(".faq-question").textContent.toLowerCase();
        const answer = item.querySelector(".faq-answer").textContent.toLowerCase();

        if (question.includes(query) || answer.includes(query)) {
          item.classList.remove("hidden");
          sectionMatches++;
          overallMatches++;
        } else {
          item.classList.add("hidden");
          // Close accordion if it was open
          const container = item.querySelector(".faq-answer-container");
          container.style.maxHeight = null;
          item.querySelector(".ri-arrow-down-s-line").style.transform = "rotate(0deg)";
        }
      });

      // Show/hide section based on matches
      if (sectionMatches > 0) {
        section.classList.remove("hidden");
      } else {
        section.classList.add("hidden");
      }
    });

    // Handle overall fallback
    if (overallMatches === 0 && query !== "") {
      noResultsDiv.classList.remove("hidden");
    } else {
      noResultsDiv.classList.add("hidden");
    }
  }

  // --- AI CHAT AGENT WIDGET ---
  const chatBubbleContainer = document.getElementById("chat-bubble-container");
  const chatBubbleTrigger = document.getElementById("chat-bubble-trigger");
  const aiChatWidget = document.getElementById("ai-chat-widget");
  const closeChatWidget = document.getElementById("close-chat-widget");
  const openChatBtn = document.getElementById("open-chat-btn");
  const chatConversation = document.getElementById("chat-conversation");
  const chatInputForm = document.getElementById("chat-input-form");
  const chatMessageInput = document.getElementById("chat-message-input");
  const clearChatHistoryBtn = document.getElementById("clear-chat-history");
  const suggestionsContainer = document.getElementById("suggestions-container");

  // Toggle open chat
  function openChat() {
    aiChatWidget.classList.remove("opacity-0", "pointer-events-none", "translate-y-4");
    aiChatWidget.classList.add("opacity-100", "translate-y-0");
    chatBubbleContainer.classList.add("scale-0", "opacity-0");
    chatMessageInput.focus();
    
    // Smoothly scroll message panel to bottom
    setTimeout(() => {
      chatConversation.scrollTop = chatConversation.scrollHeight;
    }, 300);
  }

  // Toggle close chat
  function closeChat() {
    aiChatWidget.classList.add("opacity-0", "pointer-events-none", "translate-y-4");
    aiChatWidget.classList.remove("opacity-100", "translate-y-0");
    chatBubbleContainer.classList.remove("scale-0", "opacity-0");
  }

  chatBubbleTrigger.addEventListener("click", openChat);
  openChatBtn.addEventListener("click", openChat);
  closeChatWidget.addEventListener("click", closeChat);

  if (document.getElementById("server-response")) {
    openChat();
  }

  // Clear chat history
  clearChatHistoryBtn.addEventListener("click", () => {
    chatConversation.innerHTML = `
      <div class="flex items-start gap-2.5 max-w-[85%]">
        <div class="w-8 h-8 bg-slate-200 text-slate-600 rounded-full flex items-center justify-center flex-shrink-0 text-sm">
          <i class="ri-robot-line"></i>
        </div>
        <div class="bg-white border border-slate-200/60 text-slate-800 p-3.5 rounded-2xl rounded-tl-none shadow-xs text-sm font-inter leading-relaxed">
          Chat cleared. Hello again! How can I help you plan your next journey or answer questions about your booking today?
        </div>
      </div>
    `;
  });

  // Suggestions/Quick Replies click handler
  suggestionsContainer.addEventListener("click", (e) => {
    const btn = e.target.closest(".suggestion-btn");
    if (btn) {
      chatMessageInput.value = btn.innerText.trim();
      chatInputForm.requestSubmit();
    }
  });

  // Handle Chat Input Form submission
  chatInputForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = chatMessageInput.value.trim();
    if (!text) {
      return;
    }

    const submitButton = chatInputForm.querySelector('button[type="submit"]');
    const loadingId = `chat-loading-${Date.now()}`;
    const formData = new FormData(chatInputForm);
    submitButton.disabled = true;
    chatMessageInput.value = "";
    chatConversation.insertAdjacentHTML("beforeend", `
      <div class="flex justify-end w-full">
        <div class="bg-[#051120] text-white p-3.5 rounded-2xl rounded-tr-none shadow-xs text-sm max-w-[85%] font-inter leading-relaxed">${escapeHTML(text)}</div>
      </div>
      <div id="${loadingId}" class="flex items-start gap-2.5 max-w-[85%]" aria-label="Assistant is typing">
        <div class="w-8 h-8 bg-slate-200 text-slate-600 rounded-full flex items-center justify-center flex-shrink-0 text-sm"><i class="ri-robot-line"></i></div>
        <div class="bg-white border border-slate-200/60 text-slate-800 p-3.5 px-5 rounded-2xl rounded-tl-none shadow-xs">
          <div class="flex items-center gap-1" aria-hidden="true">
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce"></span>
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
          </div>
        </div>
      </div>
    `);
    chatConversation.scrollTop = chatConversation.scrollHeight;

    try {
      const response = await fetch(chatInputForm.action, {
        method: "POST",
        body: formData,
        headers: { "X-Requested-With": "XMLHttpRequest" },
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error("Unable to get a response.");
      }

      chatConversation.insertAdjacentHTML("beforeend", `
        <div class="flex items-start gap-2.5 max-w-[85%]">
          <div class="w-8 h-8 bg-slate-200 text-slate-600 rounded-full flex items-center justify-center flex-shrink-0 text-sm"><i class="ri-robot-line"></i></div>
          <div class="bg-white border border-slate-200/60 text-slate-800 p-3.5 rounded-2xl rounded-tl-none shadow-xs text-sm font-inter leading-relaxed">${escapeHTML(data.response)}</div>
        </div>
      `);
      chatConversation.scrollTop = chatConversation.scrollHeight;
    } catch (error) {
      chatConversation.insertAdjacentHTML("beforeend", `
        <div class="text-sm text-red-600">Sorry, we could not send your question. Please try again.</div>
      `);
    } finally {
      document.getElementById(loadingId)?.remove();
      submitButton.disabled = false;
    }
  });

  function escapeHTML(str) {
    return String(str).replace(/[&<>'"]/g, tag => ({
      '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;'
    }[tag]));
  }

});
