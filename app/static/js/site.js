(() => {
  const selector = document.getElementById("siteLanguage");
  const readerLanguage = document.getElementById("readerLanguage");
  const coverLink = document.getElementById("coverLink");
  const supported = ["en", "kn"];

  function setLanguage(lang) {
    lang = supported.includes(lang) ? lang : "en";
    document.documentElement.lang = lang;

    document.querySelectorAll("[data-en][data-kn]").forEach((el) => {
      el.textContent = el.dataset[lang];
    });
    document.querySelectorAll("[data-en-html][data-kn-html]").forEach((el) => {
      el.innerHTML = el.dataset[`${lang}Html`];
    });
    document.querySelectorAll("[data-alt-en][data-alt-kn]").forEach((el) => {
      el.alt = el.dataset[lang === "kn" ? "altKn" : "altEn"];
    });

    if (selector) selector.value = lang;
    if (readerLanguage) readerLanguage.value = lang;
    if (coverLink) coverLink.href = `/reader?language=${lang}`;

    try { localStorage.setItem("kathaLokaLanguage", lang); } catch (_) {}
  }

  let initial = "en";
  try { initial = localStorage.getItem("kathaLokaLanguage") || "en"; } catch (_) {}
  setLanguage(initial);
  selector?.addEventListener("change", () => setLanguage(selector.value));
  readerLanguage?.addEventListener("change", () => {
    if (coverLink) coverLink.href = `/reader?language=${readerLanguage.value}`;
  });
  document.getElementById("readerForm")?.addEventListener("submit", () => {
    try { localStorage.setItem("kathaLokaLanguage", readerLanguage.value); } catch (_) {}
  });
})();