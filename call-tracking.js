/* Mesure des contacts — un seul écouteur délégué pour tout le site.
 * Événements GA4 : phone_click, whatsapp_click, calendly_click (sites vitrine uniquement).
 * Exactement un événement par clic : les anciens helpers inline (trackTelClick, trackPhoneClick,
 * trackWhatsAppClick) sont neutralisés pour ne pas doubler la mesure.
 */
(function () {
  if (window.__nrContactTracking) return;
  window.__nrContactTracking = true;

  var SITE = "CU";
  var CALENDLY = false; // site urgence : pas de Calendly

  window.dataLayer = window.dataLayer || [];
  function gtagSafe() {
    if (typeof window.gtag === "function") window.gtag.apply(window, arguments);
    else window.dataLayer.push(arguments);
  }
  var noop = function () {};
  window.trackTelClick = noop;
  window.trackPhoneClick = noop;
  window.trackWhatsAppClick = noop;

  // Click counter: no cookie, nothing stored on the device, no identifier. Not anonymous in the strict
  // sense: the request carries the page path, and Cloudflare receives IP + user agent technically.
  // Inactive while COUNTER_URL is empty. Filled only at deploy, after Filipe's GO.
  var COUNTER_URL = "";
  function countContact(name, pos) {
    var t = name === "phone_click" ? "tel" : name === "whatsapp_click" ? "wa" : null;
    if (!t || !COUNTER_URL || !navigator.sendBeacon) return;
    var body = JSON.stringify({ s: SITE, p: location.pathname, t: t, l: pos });
    try { navigator.sendBeacon(COUNTER_URL, new Blob([body], { type: "text/plain" })); } catch (e) {}
  }

  function kind(el) {
    var tracked = el.getAttribute("data-track");
    if (tracked === "phone_click" || tracked === "whatsapp_click") return tracked;
    var href = el.getAttribute("href") || "";
    if (/^tel:/i.test(href)) return "phone_click";
    if (/wa\.me\/|api\.whatsapp\.com\/|^whatsapp:/i.test(href)) return "whatsapp_click";
    if (CALENDLY && /calendly\.com\//i.test(href)) return "calendly_click";
    return null;
  }

  function position(el) {
    if (el.closest('[role="dialog"]')) return "popup";
    if (el.closest("header")) return "header";
    if (el.closest("footer")) return "footer";
    for (var e = el; e && e !== document.body; e = e.parentElement) {
      var p = window.getComputedStyle(e).position;
      if (p === "fixed" || p === "sticky") return "fixed";
    }
    return "body";
  }

  document.addEventListener(
    "click",
    function (ev) {
      var el = ev.target && ev.target.closest ? ev.target.closest("a[href], [data-track]") : null;
      if (!el) return;
      var name = kind(el);
      if (!name) return;
      var pos = position(el);
      gtagSafe("event", name, {
        site: SITE,
        link_url: (el.getAttribute("href") || "").split("?")[0],
        link_position: pos,
        link_text: (el.innerText || "").replace(/\s+/g, " ").trim().slice(0, 60),
        transport_type: "beacon",
      });
      countContact(name, pos);
    },
    true
  );
})();
