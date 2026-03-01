document.addEventListener("DOMContentLoaded", function () {

    const filterForms = document.querySelectorAll(".auto-submit-filters");

    filterForms.forEach(form => {

        const card = form.closest(".filter-card");
        const spinner = card ? card.querySelector(".filter-spinner") : null;

        const triggerSubmit = () => {
            if (spinner) spinner.classList.remove("d-none");
            if (card) card.classList.add("opacity-50");
            form.submit();
        };

        // Checkbox changes
        form.querySelectorAll("input[type='checkbox']").forEach(cb => {
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