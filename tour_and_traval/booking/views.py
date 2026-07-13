from django.shortcuts import render

# Mock Packages Data
PACKAGES = {
  1: {
    "name": "Goa Beach Tour",
    "price": 15000,
    "duration": "4 Days, 3 Nights",
    "image": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=800&q=80",
  },
  2: {
    "name": "Misty Peaks Trek",
    "price": 24500,
    "duration": "6 Days, 5 Nights",
    "image": "https://images.unsplash.com/photo-1454496522488-7a8e488e8606?auto=format&fit=crop&w=800&q=80",
  },
  3: {
    "name": "Backwater Bliss",
    "price": 18900,
    "duration": "5 Days, 4 Nights",
    "image": "https://images.unsplash.com/photo-1593693397690-362cb9666fc2?auto=format&fit=crop&w=800&q=80",
  },
  4: {
    "name": "Royal Rajasthan",
    "price": 32000,
    "duration": "7 Days, 6 Nights",
    "image": "https://images.unsplash.com/photo-1599661046289-e31897846e41?auto=format&fit=crop&w=800&q=80",
  },
  5: {
    "name": "Spiritual Ganges",
    "price": 12500,
    "duration": "3 Days, 2 Nights",
    "image": "https://images.unsplash.com/photo-1762513907666-29901bf5899a?w=600&auto=format&fit=crop&q=60",
  },
  6: {
    "name": "Azure Deep Diving",
    "price": 45000,
    "duration": "8 Days, 7 Nights",
    "image": "https://images.unsplash.com/photo-1544551763-46a013bb70d5?auto=format&fit=crop&w=800&q=80",
  }
}

def booking_page(request):
  return render(request, "booking/booking_page.html")

def payment_page(request, package_id: int):
  package = PACKAGES.get(package_id)
  if not package:
    package = PACKAGES[1]
  
  # Calculate taxes (e.g. 5% + ₹250 convenience fee)
  taxes = int(package["price"] * 0.05 + 250)
  total = package["price"] + taxes
  
  return render(request, "booking/payment_page.html", {
    "package": package,
    "taxes": taxes,
    "total": total,
    "package_id": package_id,
  })

def booking_success_page(request, booking_id: int, payment_id: int, transection_id: str, package_id: int):
  package = PACKAGES.get(package_id)
  if not package:
    package = PACKAGES[1]
  return render(request, "booking/booking_success_page.html", {
    "booking_id": booking_id,
    "payment_id": payment_id,
    "transection_id": transection_id,
    "package": package,
  })