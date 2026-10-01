/* Latverian Vault control script - property of Victor von Doom */
(function () {
  "use strict";

  // --- sealed constants -----------------------------------------------------
  var _k = [81, 92, 92, 90, 96, 81, 78, 102];      // first seal
  var _s = 13;
  var _m =
    "RlJBR01FTlQgMSA9IHRoZSB1cHBlcmNhc2Ugd29yZCB5b3UganVzdCByZWJ1aWx0LiBGUkFHTUVO" +
    "VCAyIGhpZGVzIGluc2lkZSBEb29tcyBTaWdpbCAoZG93bmxvYWQgaXQgYXQgL3NpZ2lsKSBzZWFs" +
    "ZWQgd2l0aCBzdGVnaGlkZS4gVGhlIHBhc3NwaHJhc2UgaXMgdGhlIG5hbWUgVmljdG9yIHZvbiBE" +
    "b29tIG1vdXJucyBhYm92ZSBhbGwgLS0gdGhlIGxvc3QgbG92ZSBoaXMgbGlmZXMgd29yayB3YXMg" +
    "bmFtZWQgZm9yLiBBc3NlbWJsZSB0aGUgQ29zbWljIEtleSBhcyBGUkFHMS1GUkFHMiB0aGVuIHNw" +
    "ZWFrIGl0IHRvIHRoZSB2YXVsdC4=";

  function _rebuild(arr, sh) {
    return arr.map(function (c) { return String.fromCharCode(c - sh); }).join("");
  }

  // FRAGMENT 1 is reconstructed here but deliberately never shown in the UI.
  var FRAG1 = _rebuild(_k, _s);

  // The guidance below is base64; Doom does not hand out plaintext.
  var GUIDE = (function () { try { return atob(_m); } catch (e) { return ""; } })();

  // --- UI wiring ------------------------------------------------------------
  var out = function (msg, cls) {
    var el = document.getElementById("result");
    el.textContent = msg;
    el.className = "result " + (cls || "");
  };

  window.__reveal = function () {
    // Easter-egg console helper for stuck reversers. Doom permits a whisper.
    console.log("%cFRAGMENT 1 whisper -> %c" + FRAG1, "color:#c9a227", "color:#fff");
    console.log("%cGUIDE -> %c" + GUIDE, "color:#c9a227", "color:#fff");
    return "Check the console, mortal.";
  };

  document.addEventListener("DOMContentLoaded", function () {
    var btn = document.getElementById("submit");
    var inp = document.getElementById("key");

    btn.addEventListener("click", function () {
      var val = (inp.value || "").trim();
      if (!val) { out("The vault hears only silence.", "err"); return; }

      // Local format pre-check so players know fragment 1 is on the right track.
      var parts = val.split("-");
      if (parts.length === 2 && parts[0] === FRAG1 && parts[1].length) {
        out("First seal accepted. Presenting the key to Doom...", "ok");
      } else if (parts.length === 2 && parts[0] === FRAG1) {
        out("First seal correct, but the second fragment is missing.", "err");
        return;
      }

      fetch("/unlock", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ key: val }),
      })
        .then(function (r) { return r.json(); })
        .then(function (d) {
          if (d.ok) { out(d.msg + "  " + d.flag, "ok"); }
          else { out(d.msg, "err"); }
        })
        .catch(function () { out("The timestream flickered. Try again.", "err"); });
    });
  });
})();
