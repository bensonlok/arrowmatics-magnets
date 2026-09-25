(function () {
  if (window.__magnetsExpertChat) return;
  window.__magnetsExpertChat = true;

  var WA =
    "https://wa.me/60122112522?text=" +
    encodeURIComponent(
      "Hi Arrowmatics Magnets — I'd like to talk to a human about magnets / separators."
    );
  var API = "/api/magnet-chat";
  var MAX_IMAGE_EDGE = 1280;
  var JPEG_QUALITY = 0.72;
  var MAX_DATA_URL_CHARS = 900000; /* ~650KB binary — keep CF / OpenRouter payloads small */
  var history = [];
  var lead = null;
  var pendingFile = null; /* { name, mime, dataUrl, previewUrl, kind: 'image'|'pdf' } */
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
    return phone.length >= 8 || /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
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
      el("p", {
        id: "magnets-expert-sub",
        text: "Photo / sketch → application-fit solution",
      }),
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

  /* ---- LEAD GATE ---- */
  var gate = el("div", { id: "magnets-expert-gate" });
  gate.appendChild(
    el("p", {
      class: "mec-gate-intro",
      text: "Leave your name and WhatsApp or email, then chat with Magnet Expert — upload a machine photo or sketch anytime.",
    })
  );
  var nameIn = el("input", {
    id: "mec-name",
    type: "text",
    placeholder: "Your name *",
    autocomplete: "name",
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
    text: "Required: name + (WhatsApp or email).",
  });
  var gateErr = el("p", { id: "mec-gate-err", class: "mec-gate-err", text: "" });
  var gateBtn = el("button", {
    id: "mec-gate-btn",
    type: "button",
    text: "Start chat",
  });
  gate.appendChild(nameIn);
  gate.appendChild(phoneIn);
  gate.appendChild(emailIn);
  gate.appendChild(gateHint);
  gate.appendChild(gateErr);
  gate.appendChild(gateBtn);

  /* ---- CHAT BODY: left messages + right upload ---- */
  var body = el("div", { id: "magnets-expert-body" });

  var leftCol = el("div", { id: "magnets-expert-left" });
  var msgs = el("div", { id: "magnets-expert-msgs" });
  var form = el("form", { id: "magnets-expert-form" });
  var input = el("input", {
    id: "magnets-expert-input",
    type: "text",
    placeholder: "Describe the duty, or send with your photo…",
    autocomplete: "off",
  });
  var send = el("button", {
    id: "magnets-expert-send",
    type: "submit",
    text: "Send",
  });
  form.appendChild(input);
  form.appendChild(send);
  leftCol.appendChild(msgs);
  leftCol.appendChild(form);

  var rightCol = el("aside", {
    id: "magnets-expert-right",
    "aria-label": "Photo or sketch upload",
  });
  var rightToggle = el("button", {
    id: "mec-upload-toggle",
    type: "button",
    "aria-expanded": "true",
    text: "Photo / sketch ▲",
  });
  var rightInner = el("div", { id: "mec-upload-inner" });
  rightInner.appendChild(
    el("h3", { class: "mec-upload-title", text: "Upload photo or sketch" })
  );
  rightInner.appendChild(
    el("p", {
      class: "mec-upload-tip",
      text: "Tip: circle or point at the problem area on the machine, hopper, pipe or drawing. Magnet Expert recommends separator / NdFeB / SmCo / lifting from what it sees — then WhatsApp for a written quote.",
    })
  );

  var drop = el("label", {
    id: "mec-drop",
    for: "mec-file",
    html:
      '<span class="mec-drop-icon" aria-hidden="true">📷</span>' +
      "<strong>Snap or choose file</strong>" +
      "<span>JPG, PNG, WebP or PDF</span>",
  });
  var fileIn = el("input", {
    id: "mec-file",
    type: "file",
    accept: "image/jpeg,image/png,image/webp,image/jpg,application/pdf,.pdf",
  });
  drop.appendChild(fileIn);

  var previewWrap = el("div", { id: "mec-preview-wrap", hidden: "hidden" });
  var previewImg = el("img", {
    id: "mec-preview-img",
    alt: "Upload preview",
  });
  var previewMeta = el("p", { id: "mec-preview-meta", text: "" });
  var clearBtn = el("button", {
    id: "mec-clear-file",
    type: "button",
    text: "Remove",
  });
  previewWrap.appendChild(previewImg);
  previewWrap.appendChild(previewMeta);
  previewWrap.appendChild(clearBtn);

  var attachStatus = el("p", { id: "mec-attach-status", text: "" });

  rightInner.appendChild(drop);
  rightInner.appendChild(previewWrap);
  rightInner.appendChild(attachStatus);
  rightCol.appendChild(rightToggle);
  rightCol.appendChild(rightInner);

  body.appendChild(rightCol);
  body.appendChild(leftCol);

  panel.appendChild(header);
  panel.appendChild(human);
  panel.appendChild(gate);
  panel.appendChild(body);
  root.appendChild(fab);
  root.appendChild(panel);
  document.body.appendChild(root);

  function addMsg(role, text, isErr, thumbUrl) {
    var m = el("div", {
      class: "mec-msg " + (isErr ? "err" : role === "user" ? "user" : "bot"),
    });
    if (thumbUrl) {
      m.appendChild(
        el("img", { class: "mec-msg-thumb", src: thumbUrl, alt: "Attached" })
      );
    }
    var t = el("div", { class: "mec-msg-text", text: text });
    m.appendChild(t);
    msgs.appendChild(m);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function showGate() {
    gate.style.display = "flex";
    body.style.display = "none";
    document.getElementById("magnets-expert-sub").textContent =
      "Photo / sketch → application-fit solution";
  }

  function showChat() {
    gate.style.display = "none";
    body.style.display = "flex";
    if (lead) {
      var bits = [lead.name];
      if (lead.phone) bits.push(lead.phone);
      if (lead.email) bits.push(lead.email);
      document.getElementById("magnets-expert-sub").textContent = bits.join(" · ");
    }
  }

  function startChat() {
    showChat();
    msgs.innerHTML = "";
    history = [];
    addMsg(
      "bot",
      "Hi " +
        (lead && lead.name ? lead.name : "") +
        " — I’m Magnet Expert for Arrowmatics Magnets (Shah Alam).\n\n" +
        "Easy as 1-2-3:\n" +
        "1) Upload a photo of your machine or a sketch (circle the problem) in the Photo / sketch panel.\n" +
        "2) Add a short description.\n" +
        "3) I’ll suggest a separator, NdFeB, SmCo or lifting fit from our range — then WhatsApp +60 12-211 2522 for a written quote.\n\n" +
        "Need a person? Tap Talk to human."
    );
    input.focus();
  }

  if (validLead(lead)) {
    if (lead.name) nameIn.value = lead.name;
    if (lead.phone) phoneIn.value = lead.phone;
    if (lead.email) emailIn.value = lead.email;
    startChat();
  } else {
    lead = null;
    try {
      localStorage.removeItem("magnets_expert_lead");
    } catch (e) {}
    showGate();
  }

  function open() {
    panel.classList.add("open");
    fab.style.display = "none";
    if (validLead(lead)) input.focus();
    else {
      showGate();
      nameIn.focus();
    }
  }
  function close() {
    panel.classList.remove("open");
    fab.style.display = "";
  }

  window.openMagnetExpert = open;
  fab.addEventListener("click", open);
  document.getElementById("magnets-expert-close").addEventListener("click", close);

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t) return;
    var btn = t.closest && t.closest("[data-open-magnet-expert]");
    if (btn) {
      e.preventDefault();
      open();
    }
  });

  gateBtn.addEventListener("click", function () {
    var next = {
      name: (nameIn.value || "").trim(),
      phone: (phoneIn.value || "").trim(),
      email: (emailIn.value || "").trim(),
    };
    if (!validLead(next)) {
      gateErr.textContent = "Enter your name and at least WhatsApp or email.";
      showGate();
      return;
    }
    gateErr.textContent = "";
    lead = next;
    try {
      localStorage.setItem("magnets_expert_lead", JSON.stringify(lead));
    } catch (e) {}
    startChat();
  });

  rightToggle.addEventListener("click", function () {
    var openNow = rightCol.classList.toggle("collapsed");
    rightToggle.setAttribute("aria-expanded", openNow ? "false" : "true");
    rightToggle.textContent = openNow ? "Photo / sketch ▼" : "Photo / sketch ▲";
  });

  function clearPending() {
    pendingFile = null;
    previewImg.removeAttribute("src");
    previewImg.style.display = "none";
    previewMeta.textContent = "";
    previewWrap.hidden = true;
    attachStatus.textContent = "";
    fileIn.value = "";
  }

  clearBtn.addEventListener("click", clearPending);

  function setPending(fileObj) {
    pendingFile = fileObj;
    previewWrap.hidden = false;
    if (fileObj.kind === "image") {
      previewImg.style.display = "block";
      previewImg.src = fileObj.previewUrl || fileObj.dataUrl;
      previewMeta.textContent = fileObj.name + " · ready to send with your next message";
    } else {
      previewImg.style.display = "none";
      previewMeta.textContent =
        "PDF: " + fileObj.name + " · will be noted with your next message";
    }
    attachStatus.textContent = "Attached — write a short description and tap Send.";
  }

  function readAsDataURL(file) {
    return new Promise(function (resolve, reject) {
      var fr = new FileReader();
      fr.onload = function () {
        resolve(fr.result);
      };
      fr.onerror = reject;
      fr.readAsDataURL(file);
    });
  }

  function compressImage(file) {
    return new Promise(function (resolve, reject) {
      var url = URL.createObjectURL(file);
      var img = new Image();
      img.onload = function () {
        var w = img.naturalWidth || img.width;
        var h = img.naturalHeight || img.height;
        var scale = Math.min(1, MAX_IMAGE_EDGE / Math.max(w, h));
        var cw = Math.max(1, Math.round(w * scale));
        var ch = Math.max(1, Math.round(h * scale));
        var canvas = document.createElement("canvas");
        canvas.width = cw;
        canvas.height = ch;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(img, 0, 0, cw, ch);
        URL.revokeObjectURL(url);
        var dataUrl = canvas.toDataURL("image/jpeg", JPEG_QUALITY);
        if (dataUrl.length > MAX_DATA_URL_CHARS) {
          dataUrl = canvas.toDataURL("image/jpeg", 0.55);
        }
        if (dataUrl.length > MAX_DATA_URL_CHARS) {
          reject(new Error("Image still too large after compression. Try a smaller photo."));
          return;
        }
        resolve({
          name: (file.name || "photo.jpg").replace(/\.[^.]+$/, "") + ".jpg",
          mime: "image/jpeg",
          dataUrl: dataUrl,
          previewUrl: dataUrl,
          kind: "image",
        });
      };
      img.onerror = function () {
        URL.revokeObjectURL(url);
        reject(new Error("Could not read that image."));
      };
      img.src = url;
    });
  }

  fileIn.addEventListener("change", function () {
    var file = fileIn.files && fileIn.files[0];
    if (!file) return;
    attachStatus.textContent = "Preparing…";
    var mime = (file.type || "").toLowerCase();
    var isPdf =
      mime === "application/pdf" || /\.pdf$/i.test(file.name || "");
    var isImage =
      /^image\/(jpeg|jpg|png|webp)$/i.test(mime) ||
      /\.(jpe?g|png|webp)$/i.test(file.name || "");

    if (!isPdf && !isImage) {
      attachStatus.textContent = "Please choose JPG, PNG, WebP or PDF.";
      fileIn.value = "";
      return;
    }

    if (isPdf) {
      if (file.size > 700000) {
        attachStatus.textContent =
          "PDF is over ~700KB. Please compress it, or snap a photo of the sketch instead.";
        fileIn.value = "";
        return;
      }
      readAsDataURL(file)
        .then(function (dataUrl) {
          if (String(dataUrl).length > MAX_DATA_URL_CHARS) {
            attachStatus.textContent =
              "PDF too large for chat. Snap a photo of the page instead.";
            return;
          }
          setPending({
            name: file.name || "sketch.pdf",
            mime: "application/pdf",
            dataUrl: dataUrl,
            previewUrl: null,
            kind: "pdf",
          });
        })
        .catch(function () {
          attachStatus.textContent = "Could not read that PDF.";
        });
      return;
    }

    compressImage(file)
      .then(setPending)
      .catch(function (err) {
        attachStatus.textContent =
          (err && err.message) || "Could not prepare that image.";
      });
  });

  function buildUserContent(text, fileObj) {
    var base =
      text ||
      (fileObj
        ? "Please review my attached photo/sketch and recommend an application-fit magnet solution from your range."
        : "");
    if (!fileObj) return base;

    if (fileObj.kind === "image") {
      return [
        { type: "text", text: base },
        { type: "image_url", image_url: { url: fileObj.dataUrl } },
      ];
    }
    /* PDF: text note + optional file part for models that accept it */
    return [
      {
        type: "text",
        text:
          base +
          "\n\n[Visitor attached PDF sketch/drawing: " +
          fileObj.name +
          ". If you cannot render the PDF, ask them to confirm what is circled and recommend from description.]",
      },
      {
        type: "file",
        file: { filename: fileObj.name, file_data: fileObj.dataUrl },
      },
    ];
  }

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    if (!validLead(lead)) {
      gateErr.textContent = "Enter your name and at least WhatsApp or email.";
      showGate();
      nameIn.focus();
      return;
    }
    var text = (input.value || "").trim();
    var fileObj = pendingFile;
    if (!text && !fileObj) return;
    input.value = "";

    var display =
      text ||
      (fileObj
        ? fileObj.kind === "pdf"
          ? "[PDF] " + fileObj.name
          : "[Photo] " + fileObj.name
        : "");
    addMsg(
      "user",
      display,
      false,
      fileObj && fileObj.kind === "image" ? fileObj.previewUrl || fileObj.dataUrl : null
    );

    var content = buildUserContent(text, fileObj);
    history.push({ role: "user", content: content });
    clearPending();
    send.disabled = true;
    attachStatus.textContent = "Magnet Expert is reviewing…";

    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        messages: history,
        lead: lead,
        notify: history.filter(function (m) {
          return m.role === "user";
        }).length === 1,
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
            "Chat offline. Use Talk to human on WhatsApp.";
          if (/name|whatsapp|email/i.test(err)) {
            gateErr.textContent = err;
            showGate();
          } else {
            addMsg("bot", err, true);
          }
          return;
        }
        var reply = res.j.reply || "";
        history.push({ role: "assistant", content: reply });
        addMsg("bot", reply);
        attachStatus.textContent = "";
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
