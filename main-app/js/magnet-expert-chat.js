(function () {
  if (window.__magnetsExpertChat) return;
  window.__magnetsExpertChat = true;

  var WA = "https://wa.me/60122112522?text=" + encodeURIComponent(
    "Hi Arrowmatics Magnets — I'd like to talk to a human about magnets / separators."
  );
  var API = "/api/magnet-chat";
  var history = [];
  var lead = null;
  try {
    lead = JSON.parse(localStorage.getItem("magnets_expert_lead") || "null");
  } catch (e) {
    lead = null;
  }

  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs)
      Object.keys(attrs).forEach(function (k) {
        if (k === "text") n.textContent = attrs[k];
        else if (k === "html") n.innerHTML = attrs[k];
        else if (k === "class") n.className = attrs[k];
        else n.setAttribute(k, attrs[k]);
      });
    (kids || []).forEach(function (c) {
      if (c) n.appendChild(c);
    });
    return n;
  }

  function validLead(L) {
    if (!L || !L.name || String(L.name).trim().length < 2) return false;
    var phone = String(L.phone || "").replace(/\s+/g, "");
    var email = String(L.email || "").trim();
    var phoneOk = phone.length >= 8;
    var emailOk = /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    return phoneOk || emailOk;
  }

  var root = el("div", { id: "magnets-expert-root" });
  var fab = el("button", {
    id: "magnets-expert-fab",
    type: "button",
    "aria-label": "Open Magnet Expert chat",
    html: "<span>Magnet<br>Expert</span>",
  });
  var panel = el("div", {
    id: "magnets-expert-panel",
    role: "dialog",
    "aria-label": "Magnet Expert",
  });
  var header = el("header", null, [
    el("div", { class: "titles" }, [
      el("h2", { text: "Magnet Expert" }),
      el("p", { id: "magnets-expert-sub", text: "Sales & technical · Arrowmatics Magnets" }),
    ]),
    el("button", {
      id: "magnets-expert-close",
      type: "button",
      "aria-label": "Close",
      text: "×",
    }),
  ]);
  var human = el("a", {
    id: "magnets-expert-human",
    href: WA,
    target: "_blank",
    rel: "noopener",
    text: "Talk to human — WhatsApp +60 12-211 2522",
  });

  var gate = el("div", { id: "magnets-expert-gate" });
  gate.appendChild(
    el("p", {
      class: "mec-gate-intro",
      text: "Before we chat, leave your name and WhatsApp or email so we can follow up on quotes.",
    })
  );
  var nameIn = el("input", {
    id: "mec-name",
    type: "text",
    placeholder: "Your name *",
    autocomplete: "name",
    required: "required",
  });
  var phoneIn = el("input", {
    id: "mec-phone",
    type: "tel",
    placeholder: "WhatsApp / mobile",
    autocomplete: "tel",
  });
  var emailIn = el("input", {
    id: "mec-email",
    type: "email",
    placeholder: "Email",
    autocomplete: "email",
  });
  var gateHint = el("p", {
    class: "mec-gate-hint",
    text: "Need at least one: WhatsApp or email.",
  });
  var gateErr = el("p", { id: "mec-gate-err", class: "mec-gate-err", text: "" });
  var gateBtn = el("button", {
    id: "mec-gate-btn",
    type: "button",
    text: "Start with Magnet Expert",
  });
  gate.appendChild(nameIn);
  gate.appendChild(phoneIn);
  gate.appendChild(emailIn);
  gate.appendChild(gateHint);
  gate.appendChild(gateErr);
  gate.appendChild(gateBtn);

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
  panel.appendChild(gate);
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

  function setChatMode(on) {
    gate.style.display = on ? "none" : "block";
    msgs.style.display = on ? "flex" : "none";
    form.style.display = on ? "flex" : "none";
    if (on && lead) {
      var bits = [lead.name];
      if (lead.phone) bits.push(lead.phone);
      if (lead.email) bits.push(lead.email);
      document.getElementById("magnets-expert-sub").textContent = bits.join(" · ");
    }
  }

  function startChat() {
    setChatMode(true);
    if (!msgs.childNodes.length) {
      addMsg(
        "bot",
        "Hi " +
          (lead.name || "") +
          " — I’m Magnet Expert for Arrowmatics Magnets (Shah Alam).\nAsk about separators, NdFeB, SmCo or lifting magnets.\n\nNeed a person? Tap Talk to human (WhatsApp)."
      );
    }
    input.focus();
  }

  if (validLead(lead)) {
    setChatMode(true);
    startChat();
  } else {
    setChatMode(false);
  }

  function open() {
    panel.classList.add("open");
    fab.style.display = "none";
    if (validLead(lead)) input.focus();
    else nameIn.focus();
  }
  function close() {
    panel.classList.remove("open");
    fab.style.display = "";
  }

  fab.addEventListener("click", open);
  document.getElementById("magnets-expert-close").addEventListener("click", close);

  gateBtn.addEventListener("click", function () {
    var next = {
      name: (nameIn.value || "").trim(),
      phone: (phoneIn.value || "").trim(),
      email: (emailIn.value || "").trim(),
    };
    if (!validLead(next)) {
      gateErr.textContent = "Enter your name and at least WhatsApp or email.";
      return;
    }
    gateErr.textContent = "";
    lead = next;
    try {
      localStorage.setItem("magnets_expert_lead", JSON.stringify(lead));
    } catch (e) {}
    startChat();
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validLead(lead)) {
      setChatMode(false);
      return;
    }
    var text = (input.value || "").trim();
    if (!text) return;
    input.value = "";
    addMsg("user", text);
    history.push({ role: "user", content: text });
    send.disabled = true;

    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: history,
        lead: lead,
        notify: history.length === 1,
      }),
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
