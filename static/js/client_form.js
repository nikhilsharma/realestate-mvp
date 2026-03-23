function toggleAreaClusterMode() {
    const requirementEl = document.getElementById("requirement");
    if (!requirementEl) return;

    const isSell = requirementEl.value === "Sell";
    const inputs = document.querySelectorAll('input[name^="area_clusters"]');

    // Remove existing listeners first (VERY IMPORTANT)
    inputs.forEach(input => {
        input.removeEventListener("change", enforceSingle);
    });

    if (isSell) {
        let checkedFound = false;

        inputs.forEach(input => {
            if (input.checked) {
                if (!checkedFound) {
                    checkedFound = true;
                } else {
                    input.checked = false;
                }
            }

            input.addEventListener("change", enforceSingle);
        });

        // Optional: ensure at least one selected
        if (!checkedFound && inputs.length > 0) {
            inputs[0].checked = true;
        }
    }
}

function enforceSingle(e) {
    const inputs = document.querySelectorAll('input[name^="area_clusters"]');

    inputs.forEach(input => {
        if (input !== e.target) {
            input.checked = false;
        }
    });
}

document.addEventListener("DOMContentLoaded", () => {
    const requirementEl = document.getElementById("requirement");
    if (!requirementEl) return;

    requirementEl.addEventListener("change", toggleAreaClusterMode);
    toggleAreaClusterMode();
});