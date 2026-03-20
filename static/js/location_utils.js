document.addEventListener("DOMContentLoaded", function () {

  const locationBtn = document.getElementById("getLocationBtn");

  if (locationBtn) {
    locationBtn.addEventListener("click", getLocation);
  }

});

function getLocation() {

  if (!navigator.geolocation) {
    alert("Geolocation not supported");
    return;
  }

  const status = document.getElementById("locationStatus");

  if (status) {
    status.textContent = "Fetching location...";
  }

  navigator.geolocation.getCurrentPosition(

    function (position) {

      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      const latInput = document.getElementById("latitude");
      const lngInput = document.getElementById("longitude");

      if (latInput) latInput.value = lat.toFixed(7);
      if (lngInput) lngInput.value = lng.toFixed(7);

      if (status) {
        status.textContent =
          `Location saved ✔ (${lat.toFixed(5)}, ${lng.toFixed(5)})`;
      }

    },

    function () {
      if (status) {
        status.textContent = "❌ Unable to fetch location";
      }
    },

    { enableHighAccuracy: true, timeout: 10000 }  // ← add options

  );
}