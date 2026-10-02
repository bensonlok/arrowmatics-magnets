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
  var JPEG_QUALITY = 0.8;
  var REQUEST_TIMEOUT_MS = 70000;
  var FALLBACK_MSG =
    "I could not answer just now. Please tap Talk to human — WhatsApp +60 12-211 2522 and send your message or photo there; we will reply with availability.";
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
    "aria-label": "Ask the Magnet Expert",
    html:
      '<span class="fab-ico" aria-hidden="true"><svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a8 8 0 0 1-11.6 7.1L4 20l1-4.6A8 8 0 1 1 21 12z"/><path d="M8.5 11h7M8.5 14h4"/></svg></span>' +
      '<span class="fab-text"><span class="fab-label">Ask the Magnet Expert</span><span class="fab-sub">Replies in 1–3 h · business hours</span></span>',
  });
  try {
    if (sessionStorage.getItem("magnets_expert_seen")) fab.className = "calm";
  } catch (e) {}
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
        text: "Get clear on the right magnetic separator type",
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

  var trust = el("ul", {
    id: "magnets-expert-trust",
    "aria-label": "What to expect",
    html:
      "<li>Photo or sketch welcome</li><li>Plain-language guidance</li><li>Real people on WhatsApp</li><li>We reply within 1–3 hours <em>(Malaysia business hours)</em></li>",
  });

  /* ---- LEAD GATE ---- */
  var gate = el("div", { id: "magnets-expert-gate" });
  gate.appendChild(
    el("p", {
      class: "mec-gate-intro",
      text: "Stop searching — ask here. Tell us who we are helping (name + WhatsApp or email) and we will guide you to the right magnetic separator. You can send a machine photo or sketch anytime.",
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
    text: "Required: name + (WhatsApp or email). Used only to answer your enquiry. We reply within 1–3 hours (Malaysia business hours).",
  });
  var gateErr = el("p", { id: "mec-gate-err", class: "mec-gate-err", text: "" });
  var gateBtn = el("button", {
    id: "mec-gate-btn",
    type: "button",
    text: "Start — guide me to the right separator",
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
      text: "Tip: circle or point at the problem area on the machine, hopper, pipe or drawing. Magnet Expert recommends separator (grate, suspension, drawer…) / NdFeB / SmCo from what it sees — then WhatsApp for a written quote.",
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
  panel.appendChild(trust);
  panel.appendChild(human);
  panel.appendChild(gate);
  panel.appendChild(body);
  root.appendChild(fab);
  root.appendChild(panel);
  document.body.appendChild(root);

  var PHOTO_NOTE = "Example photo — actual spec confirmed at quotation";
  var PHOTO_RE = /^https:\/\/(?:www\.)?magnets\.com\.my(\/images\/[A-Za-z0-9_\/.-]{1,80}\.(?:jpe?g|png|webp))$/i;

  /* Example photos from the server: same-site /images/ paths only, max 2 */
  function addPhotos(images) {
    if (!images || !images.length || !images.slice) return;
    var wrap = el("div", { class: "mec-photos" });
    var count = 0;
    images.slice(0, 2).forEach(function (im) {
      var m = im && typeof im.url === "string" ? PHOTO_RE.exec(im.url) : null;
      if (!m) return;
      var path = m[1];
      var caption = String((im && im.caption) || "Example photo").slice(0, 80);
      var a = el("a", {
        class: "mec-photo",
        href: path,
        target: "_blank",
        rel: "noopener",
        "aria-label": caption + " — open full size",
      });
      a.appendChild(el("img", { src: path, alt: caption, loading: "lazy" }));
      a.appendChild(el("span", { class: "mec-photo-cap", text: caption }));
      wrap.appendChild(a);
      count++;
    });
    if (!count) return;
    wrap.appendChild(el("div", { class: "mec-photo-note", text: PHOTO_NOTE }));
    msgs.appendChild(wrap);
    msgs.scrollTop = msgs.scrollHeight;
  }

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

  var QUICK = [
    { t: "Which separator for my powder?", q: "Which magnetic separator is right for my powder?" },
    { t: "Upload a photo of my problem", upload: true },
    { t: "Stainless 304/316 options", q: "What are my stainless steel options, 304, 316 or 316L, for a magnetic separator?" },
    { t: "Food / HACCP use", q: "I need a magnetic separator for a food line. What should I consider for HACCP / hygiene?" },
  ];
  var pendingQuestion = null;
  var pendingUpload = false;

  function removeChips() {
    var old = msgs.querySelectorAll(".mec-chips");
    for (var i = 0; i < old.length; i++) old[i].parentNode.removeChild(old[i]);
  }

  function addChips() {
    var wrap = el("div", { class: "mec-chips", role: "group", "aria-label": "Quick questions" });
    QUICK.forEach(function (c) {
      var b = el("button", { type: "button", class: "mec-chip", text: c.t });
      b.addEventListener("click", function () {
        runQuick(c);
      });
      wrap.appendChild(b);
    });
    msgs.appendChild(wrap);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function runQuick(c) {
    if (c.upload) {
      if (isSmall()) rightCol.classList.remove("collapsed");
      try {
        fileIn.click();
      } catch (e) {}
      return;
    }
    if (send.disabled) return;
    removeChips();
    input.value = c.q;
    form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
  }

  function isSmall() {
    return window.matchMedia && window.matchMedia("(max-width: 640px)").matches;
  }

  /* Optional one-tap feedback. Sends only "up"/"down" (plus the visitor's own lead on file) to the existing alert channel. */
  function addFeedback(question) {
    var row = el("div", { class: "mec-fb" });
    row.appendChild(el("span", { text: "Did this help?" }));
    var yes = el("button", { type: "button", class: "mec-fb-btn", "aria-label": "Yes, this helped", text: "👍 Yes" });
    var no = el("button", { type: "button", class: "mec-fb-btn", "aria-label": "No, this did not help", text: "👎 No" });
    function done(v) {
      yes.disabled = true;
      no.disabled = true;
      row.innerHTML = "";
      row.appendChild(
        el("span", {
          text:
            v === "up"
              ? "Thanks — glad it helped. Send a photo or WhatsApp +60 12-211 2522 when you are ready for a quote."
              : "Sorry about that. Tap Talk to human (WhatsApp) and we will help directly — or rephrase your question here.",
        })
      );
      try {
        fetch(API, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ feedback: v, lead: lead, question: v === "down" ? String(question || "").slice(0, 160) : "" }),
        }).catch(function () {});
      } catch (e) {}
    }
    yes.addEventListener("click", function () {
      done("up");
    });
    no.addEventListener("click", function () {
      done("down");
    });
    row.appendChild(yes);
    row.appendChild(no);
    msgs.appendChild(row);
    msgs.scrollTop = msgs.scrollHeight;
  }

  function showGate() {
    gate.style.display = "flex";
    body.style.display = "none";
    document.getElementById("magnets-expert-sub").textContent =
      "Get clear on the right magnetic separator type";
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
        (lead && lead.name ? lead.name : "there") +
        " — you are in the right place. I’m the Magnet Expert for Arrowmatics Magnets (Shah Alam), and we’ll guide you step by step.\n\n" +
        "Ask me anything about magnets — which separator type to choose (grate, drawer, plate, suspension / overband, liquid line, bar), NdFeB vs SmCo, stainless 304 / 316 / 316L, or food-line use. You can write in English, 中文 or Bahasa Malaysia.\n\n" +
        "Easiest start: tap a question below, or upload a photo / sketch in the Photo panel. Our team replies within 1–3 hours (Malaysia business hours) if you prefer WhatsApp +60 12-211 2522."
    );
    addChips();
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

  function open(q) {
    panel.classList.add("open");
    fab.style.display = "none";
    fab.className = "calm";
    try {
      sessionStorage.setItem("magnets_expert_seen", "1");
    } catch (e) {}
    if (typeof q === "string" && q) pendingQuestion = q;
    if (validLead(lead)) {
      input.focus();
      runPending();
    } else {
      showGate();
      nameIn.focus();
    }
  }
  function runPending() {
    if (pendingQuestion && !send.disabled) {
      var q = pendingQuestion;
      pendingQuestion = null;
      removeChips();
      input.value = q;
      form.dispatchEvent(new Event("submit", { cancelable: true, bubbles: true }));
    }
    if (pendingUpload) {
      pendingUpload = false;
      if (isSmall()) rightCol.classList.remove("collapsed");
      try {
        fileIn.click();
      } catch (e) {}
    }
  }
  function close() {
    panel.classList.remove("open");
    fab.style.display = "";
  }

  window.openMagnetExpert = open;
  fab.addEventListener("click", function () {
    open();
  });
  document.getElementById("magnets-expert-close").addEventListener("click", close);

  document.addEventListener("click", function (e) {
    var t = e.target;
    if (!t) return;
    var btn = t.closest && t.closest("[data-open-magnet-expert]");
    if (btn) {
      e.preventDefault();
      var q = btn.getAttribute("data-expert-q");
      if (btn.hasAttribute("data-expert-upload")) {
        pendingUpload = true;
        open();
      } else open(q || undefined);
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
    runPending();
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
        var dataUrl = canvas.toDataURL("image/jpeg", JPEG_QUALITY);
        /* Still large: step quality down, then shrink the picture, until it fits */
        var q = JPEG_QUALITY;
        var tries = 0;
        while (dataUrl.length > MAX_DATA_URL_CHARS && tries < 6) {
          tries++;
          if (q > 0.5) {
            q -= 0.1;
          } else {
            cw = Math.max(1, Math.round(cw * 0.8));
            ch = Math.max(1, Math.round(ch * 0.8));
            canvas.width = cw;
            canvas.height = ch;
            ctx = canvas.getContext("2d");
            ctx.drawImage(img, 0, 0, cw, ch);
          }
          dataUrl = canvas.toDataURL("image/jpeg", q);
        }
        if (dataUrl.length > MAX_DATA_URL_CHARS) {
          URL.revokeObjectURL(url);
          reject(new Error("Image still too large after compression. Try a smaller photo, or WhatsApp it to +60 12-211 2522."));
          return;
        }
        URL.revokeObjectURL(url);
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
        reject(new Error("Could not read that image (HEIC or unusual format?). Please pick a JPG/PNG, or WhatsApp it to +60 12-211 2522."));
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

    removeChips();
    var content = buildUserContent(text, fileObj);
    history.push({ role: "user", content: content });
    clearPending();
    send.disabled = true;
    attachStatus.textContent = "Magnet Expert is checking your question…";

    /* Only the newest image goes upstream; older ones are replaced by a text note (keeps payload small) */
    var lastImgIdx = -1;
    history.forEach(function (m, idx) {
      if (
        m.role === "user" &&
        Array.isArray(m.content) &&
        m.content.some(function (p) {
          return p && p.type === "image_url";
        })
      )
        lastImgIdx = idx;
    });
    var payloadMsgs = history.map(function (m, idx) {
      if (m.role === "user" && Array.isArray(m.content) && idx !== lastImgIdx) {
        var txt = m.content
          .map(function (p) {
            if (p && p.type === "text") return p.text;
            if (p && p.type === "image_url") return "[Earlier attached image]";
            if (p && p.type === "file") return "[Earlier attached file]";
            return "";
          })
          .filter(Boolean)
          .join("\n");
        return { role: "user", content: txt || "(attachment)" };
      }
      return m;
    });

    var ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
    var timer = ctrl
      ? setTimeout(function () {
          ctrl.abort();
        }, REQUEST_TIMEOUT_MS)
      : null;

    function showFallback() {
      addMsg("bot", FALLBACK_MSG, true);
      attachStatus.textContent = "";
    }

    fetch(API, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      signal: ctrl ? ctrl.signal : undefined,
      body: JSON.stringify({
        messages: payloadMsgs,
        lead: lead,
        notify: history.filter(function (m) {
          return m.role === "user";
        }).length === 1,
      }),
    })
      .then(function (r) {
        return r
          .json()
          .catch(function () {
            return {};
          })
          .then(function (j) {
            return { ok: r.ok, j: j || {} };
          });
      })
      .then(function (res) {
        var reply = typeof res.j.reply === "string" ? res.j.reply.trim() : "";
        /* Safety-classifier text is never a real answer */
        if (/^\s*(user|response)\s+safety\s*:/i.test(reply)) reply = "";
        if (res.ok && reply) {
          history.push({ role: "assistant", content: reply });
          addMsg("bot", reply, !!res.j.degraded);
          if (!res.j.degraded) {
            addPhotos(res.j.images);
            addFeedback(text);
          }
          attachStatus.textContent = "";
          return;
        }
        var err = res.j && res.j.error;
        if (err && /name|whatsapp|email/i.test(err) && /required/i.test(err)) {
          gateErr.textContent = err;
          showGate();
          return;
        }
        /* Any other failure or an empty reply: never show a blank/"(no reply)" bubble */
        showFallback();
      })
      .catch(function () {
        showFallback();
      })
      .finally(function () {
        if (timer) clearTimeout(timer);
        send.disabled = false;
      });
  });
})();
