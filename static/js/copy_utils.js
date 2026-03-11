document.addEventListener("DOMContentLoaded", function () {

  document.querySelectorAll(".wa-ref-copy").forEach((el) => {

    el.addEventListener("click", function () {

      const ref = this.dataset.ref;

      copyToClipboard(ref);

      showCopiedIndicator(this);

    });

  });

});

function copyToClipboard(text) {

  // Try modern clipboard API first
  if (navigator.clipboard && window.isSecureContext) {

    navigator.clipboard.writeText(text).catch(() => {
      fallbackCopy(text);
    });

  } else {

    fallbackCopy(text);

  }

}

function fallbackCopy(text) {

  const textarea = document.createElement("textarea");
  textarea.value = text;

  textarea.style.position = "fixed";
  textarea.style.opacity = "0";

  document.body.appendChild(textarea);

  textarea.focus();
  textarea.select();

  document.execCommand("copy");

  document.body.removeChild(textarea);

}

function showCopiedIndicator(el) {

  if (el.classList.contains("copied")) return;

  el.classList.add("copied");

  const tick = document.createElement("span");
  tick.textContent = " ✔";
  tick.className = "copy-indicator";

  el.appendChild(tick);

  setTimeout(() => {
    tick.remove();
    el.classList.remove("copied");
  }, 1200);

}