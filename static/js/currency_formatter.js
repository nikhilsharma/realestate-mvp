document.addEventListener("DOMContentLoaded", function () {

    const budgetInput = document.getElementById("budget_input");
    const preview = document.getElementById("budget_preview");

    if (!budgetInput) return;

    budgetInput.addEventListener("input", function () {

        let value = this.value.replace(/,/g, "").replace(/\D/g, "");

        if (!value) {
            preview.innerText = "";
            return;
        }

        const number = parseInt(value);

        const formatted = new Intl.NumberFormat("en-IN").format(number);

        this.value = formatted;

        preview.innerText = "₹ " + formatted;

    });

});