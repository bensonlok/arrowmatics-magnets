(function () {
  if (window.__magnetsExpertChat) return;
  window.__magnetsExpertChat = true;

  var WA = "https://wa.me/60122112522?text=" + encodeURIComponent(
    "Hi Arrowmatics Magnets — I'd like to talk to a human about magnets / separators."
  );
  var API = "/api/magnet-chat";
  var history = [];

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs) Object.keys(attrs).forEach(function (k) {
      if (k === "text") n.textContent = attrs[k];
      else if (k === "html") n.innerHTML = attrs[k];
      else if (k === "class") n.className = attrs[k];
      else n.setAttribute(k, attrs[k]);
    });
    (kids || []).forEach(function (c) { if (c) n.appendChild(c); });
    return n;
  }

  var root = el("div", { id: "magnets-expert-root" });
  var fab = el("button", {
    id: "magnets-expert-fab",
    type: "button",
    "aria-label": "Open Magnet Expert chat",
    html: "<span>Magnet<br>Expert</span>",
  });
  var panel = el("div", { id: "magnets-expert-panel", role: "dialog", "aria-label": "Magnet Expert" });
  var header = el("header", null, [
    el("div", { class: "titles" }, [
      el("h2", { text: "Magnet Expert" }),
      el("p", { text: "Sales & technical · Arrowmatics Magnets" }),
    ]),
    el("button", { id: "magnets-expert-close", type: "button", "aria-label": "Close", text: "×" }),
  ]);
  var human = el("a", {
    id: "magnets-expert-human",
    href: WA,
    target: "_blank",
    rel: "noopener",
    text: "Talk to human — WhatsApp +60 12-211 2522",
  });
  var msgs = el("div", { id: "magnets-expert-msgs" });
  var form = el("form", { id: "magnets-expert-form" });
  var input = el("input", {
    id: "magnets-expert-input",
    type: "text",
    placeholder: "Ask about separators, NdFeB, SmCo…",
    autocomplete: "off",
  });
  var send = el("button", { id: "magnets-expert-send", type: "submit", text: "Send" });
  form.appendChild(input);
  form.appendChild(send);
  panel.appendChild(header);
  panel.appendChild(human);
  panel.appendChild(msgs);
  panel.appendChild(form);
  root.appendChild(fab);
  root.appendChild(panel);
  document.body.appendChild(root);

  function addMsg(role, text, isErr) {
    var m = el("div", {
      class: "mec-msg " + (isErr ? "err" : role === "user" ? "user" : "bot"),
      text: text,
    });
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }

  addMsg(
    "bot",
    "Hi — I’m Magnet Expert for Arrowmatics Magnets (Shah Alam). Ask about separators, NdFeB, SmCo or lifting magnets.\n\nNeed a person? Tap Talk to human (WhatsApp)."
  );

  function open() {
    panel.classList.add("open");
    fab.style.display = "none";
    input.focus();
  }
  function close() {
    panel.classList.remove("open");
    fab.style.display = "";
  }

  fab.addEventListener("click", open);
  document.getElementById("magnets-expert-close").addEventListener("click", close);

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var text = (input.value || "").trim();
    if (!text) return;
    input.value = "";
    addMsg("user", text);
    history.push({ role: "user", content: text });
    send.disabled = true;

    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ messages: history }),
    })
      .then(function (r) {
        return r.json().then(function (j) {
          return { ok: r.ok, j: j };
        });
      })
      .then(function (res) {
        if (!res.ok || res.j.error) {
          var err =
            (res.j && res.j.error) ||
            "Chat offline. Please Talk to human on WhatsApp +60 12-211 2522.";
          addMsg("bot", err, true);
          return;
        }
        var reply = res.j.reply || "";
        history.push({ role: "assistant", content: reply });
        addMsg("bot", reply);
      })
      .catch(function () {
        addMsg(
          "bot",
          "Network error. Please Talk to human — WhatsApp +60 12-211 2522.",
          true
        );
      })
      .finally(function () {
        send.disabled = false;
      });
  });
})();
