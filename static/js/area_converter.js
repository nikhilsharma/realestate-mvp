document.addEventListener("DOMContentLoaded", function () {
    const sqft = document.getElementById("area_sqft");
    const sqgaj = document.getElementById("area_sqgaj");

    if (!sqft || !sqgaj) return;

    function updateSqGaj() {
        if (sqft.value) {
            sqgaj.value = (parseFloat(sqft.value) / 9).toFixed(2);
        } else {
            sqgaj.value = "";
        }
    }

    function updateSqFt() {
        if (sqgaj.value) {
            sqft.value = (parseFloat(sqgaj.value) * 9).toFixed(0);
        } else {
            sqft.value = "";
        }
    }

    sqft.addEventListener("input", updateSqGaj);
    sqgaj.addEventListener("input", updateSqFt);

    // Auto-fill on edit page load
    if (sqft.value) {
        updateSqGaj();
    }
});
