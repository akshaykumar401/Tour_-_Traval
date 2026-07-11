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
      const text = btn.innerText.trim();
      submitUserMessage(text);
    }
  });

  // Handle Chat Input Form submission
  chatInputForm.addEventListener("submit", (e) => {
    e.preventDefault();
    const text = chatMessageInput.value.trim();
    if (text) {
      submitUserMessage(text);
      chatMessageInput.value = "";
    }
  });

  // Send message and get AI answer
  function submitUserMessage(messageText) {
    // Append User Message
    const userMsgHTML = `
      <div class="flex justify-end w-full">
        <div class="bg-[#051120] text-white p-3.5 rounded-2xl rounded-tr-none shadow-xs text-sm max-w-[85%] font-inter leading-relaxed">
          ${escapeHTML(messageText)}
        </div>
      </div>
    `;
    chatConversation.insertAdjacentHTML("beforeend", userMsgHTML);
    chatConversation.scrollTop = chatConversation.scrollHeight;

    // Show Typing Indicator
    const typingIndicatorId = "typing-indicator-" + Date.now();
    const typingIndicatorHTML = `
      <div id="${typingIndicatorId}" class="flex items-start gap-2.5 max-w-[85%]">
        <div class="w-8 h-8 bg-slate-200 text-slate-600 rounded-full flex items-center justify-center flex-shrink-0 text-sm">
          <i class="ri-robot-line"></i>
        </div>
        <div class="bg-white border border-slate-200/60 text-slate-800 p-3.5 px-5 rounded-2xl rounded-tl-none shadow-xs text-sm flex items-center justify-center">
          <div class="flex items-center gap-1 py-1">
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 0ms"></span>
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 150ms"></span>
            <span class="w-1.5 h-1.5 bg-slate-400 rounded-full animate-bounce" style="animation-delay: 300ms"></span>
          </div>
        </div>
      </div>
    `;
    chatConversation.insertAdjacentHTML("beforeend", typingIndicatorHTML);
    chatConversation.scrollTop = chatConversation.scrollHeight;

    // Simulate Network Latency
    setTimeout(() => {
      // Remove Typing Indicator
      const indicatorEl = document.getElementById(typingIndicatorId);
      if (indicatorEl) indicatorEl.remove();

      // Generate Agent Response
      const reply = getAIResponse(messageText);
      
      const aiMsgHTML = `
        <div class="flex items-start gap-2.5 max-w-[85%]">
          <div class="w-8 h-8 bg-slate-200 text-slate-600 rounded-full flex items-center justify-center flex-shrink-0 text-sm">
            <i class="ri-robot-line"></i>
          </div>
          <div class="bg-white border border-slate-200/60 text-slate-800 p-3.5 rounded-2xl rounded-tl-none shadow-xs text-sm font-inter leading-relaxed">
            ${reply}
          </div>
        </div>
      `;
      chatConversation.insertAdjacentHTML("beforeend", aiMsgHTML);
      chatConversation.scrollTop = chatConversation.scrollHeight;
    }, 1000);
  }

  // Smart Context-Aware Mock AI Response Parser
  function getAIResponse(query) {
    const lower = query.toLowerCase();
    
    // Booking
    if (lower.includes("book") || lower.includes("reserve") || lower.includes("ticket") || lower.includes("how to")) {
      return "To book a tour with NextStop, follow these easy steps:<br><br>1. Browse our catalog on the <strong>Tours</strong> page.<br>2. Select your desired tour package.<br>3. Pick your dates and number of guests.<br>4. Click the 'Book Now' button and follow checkout.<br><br>Let me know if you need help finding specific packages!";
    }
    
    // Cancellations
    if (lower.includes("cancel") || lower.includes("refund") || lower.includes("policy") || lower.includes("reimburse")) {
      return "Here is our official Cancellation Policy:<br><br>• <strong>30+ days in advance:</strong> Eligible for a full 100% refund.<br>• <strong>14–29 days in advance:</strong> Eligible for a 50% refund.<br>• <strong>Less than 14 days:</strong> Non-refundable.<br><br>If NextStop cancels a tour due to weather or safety concerns, you will receive a full refund or free rescheduling.";
    }

    // Payments
    if (lower.includes("pay") || lower.includes("card") || lower.includes("method") || lower.includes("secure") || lower.includes("price")) {
      return "We accept all major credit cards (Visa, MasterCard, Amex, Discover), PayPal, Apple Pay, and Google Pay.<br><br>Our checkout is fully PCI-compliant with secure 256-bit SSL encryption to protect your billing details. We do not store credit card numbers on our database.";
    }

    // Packing / Travel info
    if (lower.includes("pack") || lower.includes("weather") || lower.includes("luggage") || lower.includes("wear")) {
      return "Packing recommendations depend on your destination! Once your tour booking is completed and confirmed, we will automatically email you a comprehensive pre-departure guide outlining packing tips, typical weather patterns, and local guidelines.";
    }

    // Travel Insurance
    if (lower.includes("insurance") || lower.includes("medical") || lower.includes("safety") || lower.includes("health")) {
      return "We highly recommend purchasing comprehensive travel insurance for any tour. This helps protect you against unexpected medical expenses, luggage delays, travel emergencies, or trip cancellations.";
    }

    // Greetings
    if (lower.includes("hello") || lower.includes("hi") || lower.includes("hey") || lower.includes("greetings") || lower.includes("sup")) {
      return "Hello! I am your NextStop AI Assistant. How can I help you plan your travel or answer questions about bookings today?";
    }

    // Speak to human/Agent
    if (lower.includes("human") || lower.includes("agent") || lower.includes("person") || lower.includes("speak") || lower.includes("support")) {
      return "I can easily connect you to our 24/7 concierge support team. Please enter your email address or phone number, and one of our human agents will reach out to you within 15 minutes!";
    }

    // Email
    if (lower.includes("@") && (lower.includes(".com") || lower.includes(".net") || lower.includes(".org"))) {
      return "Thank you! I have passed your email to our team. A customer concierge agent will contact you shortly to follow up.";
    }

    // Default Fallback
    return "I'm here to assist you with booking details, cancellation queries, secure payments, and travel prep. Feel free to ask more specifically, or click one of our quick suggestions below.";
  }

  // Escape HTML helper to prevent XSS
  function escapeHTML(str) {
    return str.replace(/[&<>'"]/g, 
      tag => ({
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        "'": '&#39;',
        '"': '&quot;'
      }[tag] || tag)
    );
  }
});
