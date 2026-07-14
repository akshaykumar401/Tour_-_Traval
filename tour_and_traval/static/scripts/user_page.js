function switchTab(tab) {
  const btnBookings = document.getElementById("tab-btn-bookings");
  const btnProfile = document.getElementById("tab-btn-profile");
  const contentBookings = document.getElementById("tab-content-bookings");
  const contentProfile = document.getElementById("tab-content-profile");

  if (tab === "bookings") {
    // Highlight bookings tab
    btnBookings.className =
      "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-white bg-[#0f2942] transition-colors text-left cursor-pointer shadow-sm";
    btnProfile.className =
      "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-655 hover:text-slate-900 hover:bg-slate-50 transition-colors text-left cursor-pointer";

    // Toggle visibility
    contentBookings.classList.remove("hidden");
    contentProfile.classList.add("hidden");
  } else {
    // Highlight profile tab
    btnProfile.className =
      "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-bold text-white bg-[#0f2942] transition-colors text-left cursor-pointer shadow-sm";
    btnBookings.className =
      "w-full flex items-center gap-3 px-4 py-3 rounded-xl text-sm font-medium text-slate-655 hover:text-slate-900 hover:bg-slate-50 transition-colors text-left cursor-pointer";

    // Toggle visibility
    contentProfile.classList.remove("hidden");
    contentBookings.classList.add("hidden");
  }
}

document.addEventListener("DOMContentLoaded", () => {
  const urlParams = new URLSearchParams(window.location.search);
  const tab = urlParams.get("tab");
  if (tab === "bookings") {
    switchTab("bookings");
  }
});

function togglePasswordVisibility(id) {
  const input = document.getElementById(id);
  const eye = document.getElementById(`eye-${id}`);
  if (input.type === "password") {
    input.type = "text";
    eye.classList.remove("ri-eye-line");
    eye.classList.add("ri-eye-off-line");
  } else {
    input.type = "password";
    eye.classList.remove("ri-eye-off-line");
    eye.classList.add("ri-eye-line");
  }
}