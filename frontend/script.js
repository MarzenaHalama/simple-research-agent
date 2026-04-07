const form = document.getElementById("research-form");
const promptInput = document.getElementById("prompt");
const loadingSection = document.getElementById("loading-section");
const loadingText = document.getElementById("loading-text");
const resultSection = document.getElementById("result-section");
const resultContent = document.getElementById("result-content");

function setLoading(on) {
  promptInput.disabled = on;
  loadingSection.classList.toggle("hidden", !on);
}

form.addEventListener("submit", function (e) {
  e.preventDefault();

  var prompt = promptInput.value.trim();
  if (!prompt) return;

  resultSection.classList.add("hidden");
  resultContent.textContent = "";
  setLoading(true);
  loadingText.textContent = "Searching...";

  fetch("/research/stream", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt: prompt }),
  })
    .then(function (response) {
      var reader = response.body.getReader();
      var decoder = new TextDecoder();
      var buffer = "";
      var lastUpdate = null;

      function read() {
        reader.read().then(function (result) {
          if (result.done) {
            if (lastUpdate) {
              var cleanText = lastUpdate.text
                .replace(/FINISHED: TRUE/gi, "")
                .trim();
              resultContent.textContent = cleanText;
              resultSection.classList.remove("hidden");
            }
            setLoading(false);
            return;
          }

          buffer += decoder.decode(result.value, { stream: true });
          var lines = buffer.split("\n");
          buffer = lines.pop();

          for (var i = 0; i < lines.length; i++) {
            if (lines[i].startsWith("data: ")) {
              try {
                var update = JSON.parse(lines[i].slice(6));
                lastUpdate = update;
                loadingText.textContent =
                  "Iteration " + update.iteration + " of " + update.total + "...";
              } catch (err) {
                /* skip */
              }
            }
          }

          read();
        });
      }

      read();
    })
    .catch(function (err) {
      loadingText.textContent = "Error: " + err.message;
      setLoading(false);
    });
});
