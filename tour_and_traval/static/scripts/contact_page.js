document.addEventListener("DOMContentLoaded", () => {
  // Initialize map centered at Ranchi, Jharkhand, India
  const map = L.map("map", {
    zoomControl: false, // Custom position zoom control
  }).setView([23.37, 85.43], 13);

  // Add OpenStreetMap tiles
  L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
    maxZoom: 19,
    attribution:
      '&copy; <a href="https://openstreetmap.org/copyright">OpenStreetMap</a> contributors',
  }).addTo(map);

  // Custom positioned zoom control
  L.control
    .zoom({
      position: "bottomleft",
    })
    .addTo(map);

  // Custom marker icon to match theme branding
  const customIcon = L.divIcon({
    className: "custom-map-marker",
    html: `
        <div class="relative flex items-center justify-center">
          <span class="absolute w-8 h-8 bg-amber-500/35 rounded-full animate-ping"></span>
          <span class="absolute w-4 h-4 bg-[#8c5a24] rounded-full border-2 border-white shadow-md"></span>
        </div>
      `,
    iconSize: [24, 24],
    iconAnchor: [12, 12],
  });

  // Add marker at Ranchi Coordinates
  const marker = L.marker([23.37, 85.43], { icon: customIcon }).addTo(map);

  // Add info popup
  marker
    .bindPopup(
      `
      <div class="p-2 text-slate-800 font-inter">
        <h4 class="font-bold text-sm text-[#051120] font-outfit mb-0.5">NextStop HQ</h4>
        <p class="text-[11px] text-slate-500 leading-normal">Ranchi, Jharkhand, India</p>
      </div>
    `,
      {
        closeButton: false,
        offset: L.point(0, -6),
      },
    )
    .openPopup();

  // Form feedback
  document.querySelector("form").addEventListener("submit", (e) => {
    e.preventDefault();
    alert("Thank you for reaching out! Our team will contact you shortly.");
    e.target.reset();
  });
});
