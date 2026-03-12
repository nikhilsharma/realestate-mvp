document.addEventListener("DOMContentLoaded", function () {
  const panel = document.getElementById("filterPanel");
  const filterToggle = document.getElementById("filterToggle");

  if (!panel) return;

  const savedState = localStorage.getItem("filters_open");

  // Count active filters
  function getFilterCount() {
    const params = new URLSearchParams(window.location.search);

    let count = 0;

    params.forEach((value, key) => {
      if (key === "search" && value !== "") {
        count++;
      }

      if (["area_cluster", "configuration", "mode", "tags"].includes(key)) {
        count++;
      }

      if (key === "freshness" && !["fresh", "aging"].includes(value)) {
        count++;
      }

      if (key === "is_available" && value !== "true") {
        count++;
      }
    });

    return count;
  }

  const filterCount = getFilterCount();

  const filterToggleText = document.getElementById("filterToggleText");
  // Update button text
  if (filterToggleText) {
    if (filterCount > 0) {
      filterToggleText.textContent = `Filters (${filterCount})`;
    } else {
      filterToggleText.textContent = "Filters";
    }
  }

  // Detect active filters from URL
  function hasActiveFilters() {
    const params = new URLSearchParams(window.location.search);

    if (params.has("search") && params.get("search") !== "") {
      return true;
    }

    const keys = [
      "area_cluster",
      "configuration",
      "mode",
      "freshness",
      "is_available",
      "tags",
    ];

    return keys.some((key) => params.has(key));
  }

  // Restore panel state
  if (hasActiveFilters()) {
    panel.classList.add("show");
  } else if (savedState === "true") {
    panel.classList.add("show");
  } else if (savedState === "false") {
    panel.classList.remove("show");
  } else {
    if (window.innerWidth < 768) {
      panel.classList.remove("show");
    }
  }

  // Save state when collapse opens
  panel.addEventListener("shown.bs.collapse", function () {
    localStorage.setItem("filters_open", "true");
  });

  // Save state when collapse closes
  panel.addEventListener("hidden.bs.collapse", function () {
    localStorage.setItem("filters_open", "false");
  });

  const filterForms = document.querySelectorAll(".auto-submit-filters");

  filterForms.forEach((form) => {
    const card = form.closest(".filter-card");
    const spinner = card ? card.querySelector(".filter-spinner") : null;

    const triggerSubmit = () => {
      setTimeout(() => {
        if (spinner) spinner.classList.remove("d-none");
      }, 250);
      if (card) card.classList.add("opacity-50");
      form.submit();
    };

    // Checkbox changes
    form.querySelectorAll("input[type='checkbox']").forEach((cb) => {
      cb.addEventListener("change", triggerSubmit);
    });

    // Optional: submit on Enter for search input
    const searchInput = form.querySelector("input[name='search']");
    if (searchInput) {
      searchInput.addEventListener("keydown", function (e) {
        if (e.key === "Enter") {
          e.preventDefault();
          triggerSubmit();
        }
      });
    }
  });
});
