// app/static/js/main.js

// Wait until the DOM is fully loaded
document.addEventListener("DOMContentLoaded", () => {
  // Grab references to DOM elements
  const codeUploadCard = document.getElementById("code-upload-card");
  const codeInput = document.getElementById("code-file");
  const codeFilename = document.getElementById("code-filename");

  const standardsUploadCard = document.getElementById("standards-upload-card");
  const standardsInput = document.getElementById("standards-file");
  const standardsFilename = document.getElementById("standards-filename");

  const reviewBtn = document.getElementById("review-btn");
  const outputDiv = document.getElementById("output");

  let codeFile = null;
  let standardsFile = null;

  // Helper: Enable or disable the Review button
  function updateReviewButtonState() {
    if (codeFile && standardsFile) {
      reviewBtn.classList.add("enabled");
      reviewBtn.removeAttribute("disabled");
    } else {
      reviewBtn.classList.remove("enabled");
      reviewBtn.setAttribute("disabled", "true");
    }
  }

  // When the code‐card is clicked, trigger the hidden file input
  codeUploadCard.addEventListener("click", () => {
    codeInput.click();
  });

  // When a file is selected in the code input
  codeInput.addEventListener("change", () => {
    if (codeInput.files.length > 0) {
      codeFile = codeInput.files[0];
      codeFilename.textContent = `Selected: ${codeFile.name}`;
    } else {
      codeFile = null;
      codeFilename.textContent = "";
    }
    updateReviewButtonState();
  });

  // When the standards‐card is clicked, trigger its hidden input
  standardsUploadCard.addEventListener("click", () => {
    standardsInput.click();
  });

  // When a file is selected in the standards input
  standardsInput.addEventListener("change", () => {
    if (standardsInput.files.length > 0) {
      standardsFile = standardsInput.files[0];
      standardsFilename.textContent = `Selected: ${standardsFile.name}`;
    } else {
      standardsFile = null;
      standardsFilename.textContent = "";
    }
    updateReviewButtonState();
  });

  // When "Review My Code" button is clicked
  reviewBtn.addEventListener("click", async () => {
    // If button is disabled, do nothing
    if (reviewBtn.hasAttribute("disabled")) return;

    // Clear previous output
    outputDiv.innerHTML = "";

    // Show a simple loading message
    const loadingMsg = document.createElement("div");
    loadingMsg.innerHTML = '<span class="loading"></span>Running AI review… please wait…';
    loadingMsg.style.color = "#555555";
    outputDiv.appendChild(loadingMsg);

    // Build FormData with both files
    const formData = new FormData();
    formData.append("code_file", codeFile);
    formData.append("standards_file", standardsFile);

    try {
      // Send to /review endpoint (FastAPI backend)
      const response = await fetch("/review", {
        method: "POST",
        body: formData,
      });

      // If the server returns an error code, show it
      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Unknown server error");
      }

      // Parse JSON { review, suggested_fix, score }
      const result = await response.json();
      const reviewMd = result.review || "";
      const fixMd = result.suggested_fix || "";
      const score = result.score;

      // Convert Markdown → HTML (using Marked.js)
      const reviewHtml = marked.parse(reviewMd);
      const fixHtml = marked.parse(fixMd);

      // Clear loading message
      outputDiv.innerHTML = "";

      // If there is a numeric score, show it at the top
      if (score !== null && !isNaN(Number(score))) {
        const scoreBox = document.createElement("div");
        scoreBox.className = "score-box";
        scoreBox.textContent = `Code Quality Score: ${Number(score).toFixed(2)} / 1.00`;
        outputDiv.appendChild(scoreBox);
      }

      // Show the “Review Comments” section
      const reviewSection = document.createElement("div");
      reviewSection.className = "review-content";
      reviewSection.innerHTML = `<h2>📝 Review Comments</h2>${reviewHtml}`;
      outputDiv.appendChild(reviewSection);

      // Show the “Suggested Fix” section (if any)
      if (fixMd.trim()) {
        const fixSection = document.createElement("div");
        fixSection.className = "fix-content";
        fixSection.innerHTML = `<h2>🔧 Suggested Fix</h2>${fixHtml}`;
        outputDiv.appendChild(fixSection);
      }
    } catch (err) {
      // Show a user-friendly error box
      outputDiv.innerHTML = `<div class="error">⚠️ ${err.message}</div>`;
    }
  });
});
