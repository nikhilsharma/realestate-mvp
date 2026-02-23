document.addEventListener("DOMContentLoaded", function () {

    const filterForms = document.querySelectorAll(".auto-submit-filters");

    filterForms.forEach(form => {
        const checkboxes = form.querySelectorAll("input[type='checkbox']");

        checkboxes.forEach(cb => {
            cb.addEventListener("change", function () {
                form.submit();
            });
        });
    });

});