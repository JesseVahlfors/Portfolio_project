// Making a onSubmit function to satisy recaptcha
window.onSubmit = async function (token) {
  const form = document.getElementById("contactForm");
  const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

  // put token into hidden input
  let t = document.getElementById("g-recaptcha-response");
  if (!t) {
    t = document.createElement("input");
    t.type = "hidden";
    t.name = "g-recaptcha-response";
    t.id = "g-recaptcha-response";
    form.appendChild(t);
  }
  t.value = token;

  const formData = new FormData(form);
  const resp = await fetch(form.action, {
    method: "POST",
    body: formData,
    headers: {
      "X-Requested-With": "XMLHttpRequest",
      "X-CSRFToken": csrfToken
    }
  });

  const result = await resp.json().catch(() => ({}));
  const messageContainer = document.getElementById("message-container");
  messageContainer.style.display = "block";
  messageContainer.textContent = "";
  const div = document.createElement("div");
  div.className = "message p-4 rounded-lg mb-4";

  if (resp.ok) {
    div.textContent = result.message || "Thanks for contacting me!";
    div.style.backgroundColor = "#7CFC00";
    div.style.color = "#000080";
    form.reset();
  } else {
    const errs = result.errors
      ? Object.entries(result.errors).flatMap(([f, m]) =>
          (Array.isArray(m) ? m : [m]).map(x => `${f}: ${x}`)
        ).join(" | ")
      : (result.message || "Something went wrong.");
    div.textContent = errs;
    div.style.backgroundColor = "red";
    div.style.color = "white";
  }
  messageContainer.appendChild(div);

  // Allow another submission
  if (typeof grecaptcha !== "undefined") grecaptcha.reset();
};
