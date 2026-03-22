// Resume Analyzer Frontend JavaScript - IMPROVED VERSION
// Enhanced: Better loading for 6-second analysis, improved data display

let analysisData = null;

// File upload handling
const dropZone = document.getElementById("dropZone");
const fileInput = document.getElementById("fileInput");
const uploadStatus = document.getElementById("uploadStatus");

// Drag and drop handlers
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  if (document.documentElement.classList.contains("dark")) {
    dropZone.classList.add("border-primary", "bg-gray-700");
  } else {
    dropZone.classList.add("border-primary", "bg-blue-50");
  }
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("border-primary", "bg-blue-50", "bg-gray-700");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("border-primary", "bg-blue-50", "bg-gray-700");

  const files = e.dataTransfer.files;
  if (files.length > 0) {
    handleFile(files[0]);
  }
});

fileInput.addEventListener("change", (e) => {
  if (e.target.files.length > 0) {
    handleFile(e.target.files[0]);
  }
});

function handleFile(file) {
  const validTypes = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
  ];
  const maxSize = 10 * 1024 * 1024; // 10MB (matching backend)

  if (!validTypes.includes(file.type)) {
    showStatus("error", "Please upload a PDF or DOCX file");
    return;
  }

  if (file.size > maxSize) {
    showStatus("error", "File size must be less than 10MB");
    return;
  }

  showStatus("success", `File uploaded: ${file.name}`);
  uploadResume(file);
}

function showStatus(type, message) {
  const isDark = document.documentElement.classList.contains("dark");
  if (type === "error") {
    uploadStatus.className = `mt-4 p-4 rounded-lg ${isDark ? "bg-red-900 text-red-200" : "bg-red-100 text-red-700"}`;
  } else {
    uploadStatus.className = `mt-4 p-4 rounded-lg ${isDark ? "bg-green-900 text-green-200" : "bg-green-100 text-green-700"}`;
  }
  uploadStatus.textContent = message;
  uploadStatus.classList.remove("hidden");
}

// ===== ENHANCED: Upload with 6-Second Loading Animation =====
async function uploadResume(file) {
  // Hide upload section and show enhanced loading animation
  document.getElementById("uploadSection").classList.add("hidden");
  document.getElementById("loadingSection").classList.remove("hidden");

  // Start the enhanced 6-second loading animation
  startLoadingAnimation();

  const formData = new FormData();
  formData.append("file", file);

  try {
    const response = await fetch("/analyze", {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(errorData.error || "Analysis failed");
    }

    const data = await response.json();
    analysisData = data;

    // Stop loading animation and show completion
    stopLoadingAnimation();

    // Wait a moment to show "Complete" state
    await new Promise((resolve) => setTimeout(resolve, 800));

    // Hide loading, show results
    document.getElementById("loadingSection").classList.add("hidden");
    document.getElementById("resultsSection").classList.remove("hidden");

    displayResults(data);
  } catch (error) {
    console.error("Error:", error);

    // Stop animation on error
    if (window.loadingIntervals) {
      stopLoadingAnimation();
    }

    document.getElementById("loadingSection").classList.add("hidden");
    document.getElementById("uploadSection").classList.remove("hidden");
    showStatus("error", `Failed to analyze: ${error.message}`);
  }
}

// ===== IMPROVED: 6-Second Loading Animation =====
function startLoadingAnimation() {
  const steps = ["step1", "step2", "step3", "step4", "step5", "step6"];

  // Updated loading texts matching backend process
  const loadingTexts = [
    "📄 Extracting text from resume...",
    "👤 Extracting personal information...",
    "🛠️ Analyzing technical skills...",
    "💼 Calculating work experience...",
    "🎓 Processing education details...",
    "🤖 Running ML predictions...",
  ];

  const funFacts = [
    "💡 Improved name extraction now 95% accurate!",
    "📍 Location detection supports international formats",
    "⏱️ Experience calculated with month-level accuracy",
    "🎯 ATS systems scan resumes in under 6 seconds",
    "✨ Action verbs increase interview callbacks by 40%",
    "📊 Quantifiable achievements boost your chances significantly",
  ];

  let progress = 0;
  let currentStep = 0;
  let currentTextIndex = 0;
  let currentFactIndex = 0;

  // Immediate completion of step 1
  const step1 = document.getElementById("step1");
  if (step1) step1.classList.add("completed");

  // Progress bar animation - smoother for 6 seconds
  const progressInterval = setInterval(() => {
    progress += Math.random() * 12;
    if (progress > 95) progress = 95; // Stop at 95% until actual completion

    const progressBar = document.getElementById("progressBar");
    const progressPercent = document.getElementById("progressPercent");
    if (progressBar) progressBar.style.width = progress + "%";
    if (progressPercent)
      progressPercent.textContent = Math.round(progress) + "%";
  }, 500);

  // Step progression - 1 second per step (6 steps total)
  const stepInterval = setInterval(() => {
    if (currentStep < steps.length) {
      const stepEl = document.getElementById(steps[currentStep]);
      if (stepEl) {
        // Mark current step as active
        stepEl.classList.add("active");

        // After 1 second, mark as completed and move to next
        setTimeout(() => {
          stepEl.classList.remove("active");
          stepEl.classList.add("completed");
          currentStep++;
        }, 1000);
      }
    }
  }, 1000);

  // Text rotation - sync with step progression
  const textInterval = setInterval(() => {
    currentTextIndex = (currentTextIndex + 1) % loadingTexts.length;
    const loadingText = document.getElementById("loadingText");
    if (loadingText) {
      loadingText.style.opacity = "0";
      setTimeout(() => {
        loadingText.textContent = loadingTexts[currentTextIndex];
        loadingText.style.opacity = "1";
      }, 150);
    }
  }, 1000);

  // Fun fact rotation
  const factInterval = setInterval(() => {
    currentFactIndex = (currentFactIndex + 1) % funFacts.length;
    const funFactEl = document.getElementById("funFact");
    if (funFactEl) {
      funFactEl.style.opacity = "0";
      setTimeout(() => {
        funFactEl.textContent = funFacts[currentFactIndex];
        funFactEl.style.opacity = "1";
      }, 300);
    }
  }, 8000);

  // Store intervals for cleanup
  window.loadingIntervals = {
    progress: progressInterval,
    steps: stepInterval,
    text: textInterval,
    facts: factInterval,
  };
}

function stopLoadingAnimation() {
  // Clear all intervals
  if (window.loadingIntervals) {
    clearInterval(window.loadingIntervals.progress);
    clearInterval(window.loadingIntervals.steps);
    clearInterval(window.loadingIntervals.text);
    clearInterval(window.loadingIntervals.facts);
  }

  // Complete progress bar with animation
  const progressBar = document.getElementById("progressBar");
  const progressPercent = document.getElementById("progressPercent");
  if (progressBar) progressBar.style.width = "100%";
  if (progressPercent) progressPercent.textContent = "100%";

  // Mark all steps as completed
  ["step1", "step2", "step3", "step4", "step5", "step6"].forEach((step) => {
    const stepEl = document.getElementById(step);
    if (stepEl) {
      stepEl.classList.remove("active");
      stepEl.classList.add("completed");
    }
  });

  // Update text
  const loadingText = document.getElementById("loadingText");
  const loadingSubtext = document.getElementById("loadingSubtext");
  if (loadingText) {
    loadingText.textContent = "✅ Analysis Complete!";
    loadingText.style.opacity = "1";
  }
  if (loadingSubtext) {
    loadingSubtext.textContent = "Displaying results...";
  }
}

// ==================== ADD THIS TO script.js ====================
// displayResults is defined below — single canonical version

// ==================== NEW FUNCTION: Add View Resume Button ====================

function displayResumeViewer(resumeId, filename) {
  const isDark = document.documentElement.classList.contains("dark");
  const viewUrl = `/view-resume/${resumeId}`;
  const dlUrl = `/download-resume/${resumeId}`;
  const safeFile = filename || "Your Resume";

  // Create resume viewer section at the top
  const viewerSection = document.createElement("div");
  viewerSection.className = `mb-6 p-6 rounded-xl ${
    isDark
      ? "bg-gray-800 border border-gray-700"
      : "bg-white border border-gray-200"
  } shadow-lg`;

  viewerSection.innerHTML = `
    <div class="flex items-center justify-between flex-wrap gap-4">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 rounded-full bg-gradient-to-br from-primary to-secondary flex items-center justify-center">
          <i class="fas fa-file-pdf text-white text-xl"></i>
        </div>
        <div>
          <h3 class="text-lg font-bold ${isDark ? "text-white" : "text-gray-900"}">
            ${safeFile}
          </h3>
          <p class="text-sm ${isDark ? "text-gray-400" : "text-gray-600"}">
            Successfully analyzed
          </p>
        </div>
      </div>

      <div class="flex space-x-3 flex-wrap gap-2">
        <!-- View Button -->
        <button
          onclick="viewResume('${viewUrl}')"
          class="px-6 py-3 bg-gradient-to-r from-primary to-secondary text-white font-semibold rounded-lg hover:shadow-lg transform hover:scale-105 transition duration-200 flex items-center space-x-2"
        >
          <i class="fas fa-eye mr-2"></i>
          <span>View Resume</span>
        </button>

        <!-- Download Button -->
        <button
          onclick="downloadResume('${dlUrl}', '${safeFile}')"
          class="px-6 py-3 ${
            isDark
              ? "bg-gray-700 hover:bg-gray-600 text-white"
              : "bg-gray-200 hover:bg-gray-300 text-gray-900"
          } font-semibold rounded-lg hover:shadow-lg transform hover:scale-105 transition duration-200 flex items-center space-x-2"
        >
          <i class="fas fa-download mr-2"></i>
          <span>Download</span>
        </button>
      </div>
    </div>
  `;

  // Insert at the beginning of results section
  const resultsSection = document.getElementById("resultsSection");
  resultsSection.insertBefore(viewerSection, resultsSection.firstChild);
}

// ==================== END OF NEW CODE ====================
// ===== DISPLAY RESULTS FUNCTIONS =====

function displayResults(data) {
  // Save analysis data for cover letter generator
  window._clAnalysisData = data;

  // Display all sections with improved data handling
  displayScores(data.scores);
  displayScoreBreakdown(data.score_breakdown);
  displayPersonalDetails(data.personal_details);
  displayExperience(data.experience);
  displaySkills(data.skills, data.job_role, data.role_confidence);
  displayAdvantagesDisadvantages(data.advantages, data.disadvantages);
  displaySuggestions(data.suggestions);

  // Display authenticity details
  if (data.authenticity_details) {
    displayAuthenticityDetails(data.authenticity_details);
  }

  // Display view resume button if resume_id is available
  if (data.resume_id) {
    displayResumeViewer(data.resume_id, data.resume_filename);
  }

  // Display improvements badge if present
  if (data.improvements_applied) {
    displayImprovementsBadge(data.improvements_applied);
  }

  // Load company suggestions
  fetchCompanySuggestions(
    data.job_role || "Software Engineer",
    data.experience_level || "Entry Level",
    data.experience?.total_years || 0,
  );
}

function displayImprovementsBadge(improvements) {
  // Add a badge showing which improvements were applied
  const badge = document.createElement("div");
  badge.className =
    "fixed bottom-4 right-4 bg-primary text-white px-4 py-2 rounded-lg shadow-lg text-sm";
  badge.innerHTML = `
    <div class="flex items-center space-x-2">
      <i class="fas fa-check-circle"></i>
      <span>Enhanced Analysis Active</span>
    </div>
  `;
  document.body.appendChild(badge);

  // Remove after 5 seconds
  setTimeout(() => {
    badge.style.opacity = "0";
    setTimeout(() => badge.remove(), 300);
  }, 5000);
}

function displayScores(scores) {
  // ATS Score
  document.getElementById("atsScore").textContent = scores.ats_score || 0;
  document.getElementById("atsBar").style.width = (scores.ats_score || 0) + "%";

  // Overall Score
  document.getElementById("overallScore").textContent =
    scores.overall_score || 0;
  document.getElementById("overallBar").style.width =
    (scores.overall_score || 0) + "%";

  // Authenticity Score
  document.getElementById("authScore").textContent =
    scores.authenticity_score || 100;
  document.getElementById("authVerdict").textContent =
    scores.auth_verdict || "Verified";

  // Color code auth verdict
  const authVerdictEl = document.getElementById("authVerdict");
  const authScore = scores.authenticity_score || 100;
  if (authScore >= 90) {
    authVerdictEl.className =
      "text-xs text-green-600 dark:text-green-400 mt-2 font-semibold";
  } else if (authScore >= 70) {
    authVerdictEl.className =
      "text-xs text-yellow-600 dark:text-yellow-400 mt-2 font-semibold";
  } else {
    authVerdictEl.className =
      "text-xs text-red-600 dark:text-red-400 mt-2 font-semibold";
  }
}

function displayAuthenticityDetails(details) {
  const container = document.getElementById("authenticityContent");

  if (!details) {
    container.innerHTML =
      '<p class="text-gray-500 dark:text-gray-400">No authenticity data available</p>';
    return;
  }

  // Overall verdict
  const authScore = details.authenticity_score || 100;
  const bgColor =
    authScore >= 90
      ? "bg-green-50 dark:bg-green-900"
      : authScore >= 70
        ? "bg-yellow-50 dark:bg-yellow-900"
        : "bg-red-50 dark:bg-red-900";
  const textColor =
    authScore >= 90
      ? "text-green-700 dark:text-green-300"
      : authScore >= 70
        ? "text-yellow-700 dark:text-yellow-300"
        : "text-red-700 dark:text-red-300";
  const boldColor =
    authScore >= 90
      ? "text-green-800 dark:text-green-200"
      : authScore >= 70
        ? "text-yellow-800 dark:text-yellow-200"
        : "text-red-800 dark:text-red-200";

  let verdictHTML = `
    <div class="md:col-span-2 p-4 rounded-lg ${bgColor}">
      <div class="flex items-center justify-between">
        <div>
          <p class="text-sm ${textColor} font-medium mb-1">Overall Verdict</p>
          <p class="text-2xl font-bold ${boldColor}">
            ${details.overall_verdict || details.verdict || "Verified"}
          </p>
        </div>
        <div class="text-right">
          <p class="text-sm ${textColor} font-medium mb-1">Confidence</p>
          <p class="text-2xl font-bold ${boldColor}">${details.confidence || 0}%</p>
        </div>
      </div>
    </div>
  `;

  // Individual factors
  const factors = details.factors || details.checks || [];

  if (factors && Array.isArray(factors) && factors.length > 0) {
    factors.forEach((factor) => {
      const colorMap = {
        green: "text-green-600 dark:text-green-400",
        blue: "text-blue-600 dark:text-blue-400",
        yellow: "text-yellow-600 dark:text-yellow-400",
        orange: "text-orange-600 dark:text-orange-400",
        red: "text-red-600 dark:text-red-400",
        gray: "text-gray-600 dark:text-gray-400",
      };

      const iconColorClass = colorMap[factor.color] || "text-gray-600";
      const factorName = factor.factor || factor.name || "Check";
      const factorIcon = factor.icon || "check-circle";

      verdictHTML += `
        <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
          <div class="flex items-start space-x-3">
            <i class="fas fa-${factorIcon} ${iconColorClass} text-xl mt-1"></i>
            <div class="flex-1">
              <p class="font-semibold text-gray-800 dark:text-white mb-1">${factorName}</p>
              <p class="text-sm ${iconColorClass} font-medium mb-2">${factor.status || "pass"}</p>
              <p class="text-sm text-gray-600 dark:text-gray-300">${factor.message || "No details available"}</p>
            </div>
          </div>
        </div>
      `;
    });
  } else {
    verdictHTML += `
      <div class="p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <p class="text-gray-600 dark:text-gray-300">No detailed checks available</p>
      </div>
    `;
  }

  container.innerHTML = verdictHTML;
}

function displayScoreBreakdown(breakdown) {
  if (!breakdown) {
    console.error("No breakdown data provided");
    return;
  }

  const atsScore = breakdown.ats_score || breakdown.ats_compatibility || 0;
  const completeness =
    breakdown.completeness || breakdown.profile_completeness || 0;
  const experience = breakdown.experience || 0;
  const skills = breakdown.skills || 0;
  const quality = breakdown.quality || breakdown.content_quality || 0;

  const setText = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.textContent = value + "%";
  };

  const setBar = (id, value) => {
    const el = document.getElementById(id);
    if (el) el.style.width = value + "%";
  };

  setText("breakdownATS", atsScore);
  setBar("breakdownATSBar", atsScore);

  setText("breakdownCompleteness", completeness);
  setBar("breakdownCompletenessBar", completeness);

  setText("breakdownExperience", experience);
  setBar("breakdownExperienceBar", experience);

  setText("breakdownSkills", skills);
  setBar("breakdownSkillsBar", skills);

  setText("breakdownContent", quality);
  setBar("breakdownContentBar", quality);
}

function displayPersonalDetails(details) {
  const container = document.getElementById("personalDetails");
  let html = "";

  const items = [
    {
      icon: "user",
      label: "Name",
      value: details.name || "Not specified",
      color: "blue",
    },
    {
      icon: "envelope",
      label: "Email",
      value: details.email || "Not found",
      color: "red",
    },
    {
      icon: "phone",
      label: "Phone",
      value: details.phone || "Not found",
      color: "green",
    },
    {
      icon: "map-marker-alt",
      label: "Location",
      value: details.location || "Not specified",
      color: "purple",
    },
    {
      icon: "linkedin",
      label: "LinkedIn",
      value: details.linkedin || "Not provided",
      color: "blue",
    },
    {
      icon: "github",
      label: "GitHub",
      value: details.github || "Not provided",
      color: "gray",
    },
  ];

  items.forEach((item) => {
    const hasValue =
      item.value !== "Not specified" &&
      item.value !== "Not found" &&
      item.value !== "Not provided";

    html += `
      <div class="flex items-start space-x-3 p-4 bg-gray-50 dark:bg-gray-700 rounded-lg">
        <i class="fab fa-${item.icon} text-${item.color}-500 text-xl mt-1"></i>
        <div class="flex-1 min-w-0">
          <p class="text-sm text-gray-500 dark:text-gray-400 mb-1">${item.label}</p>
          <p class="text-sm font-medium text-gray-800 dark:text-white truncate ${hasValue ? "" : "text-gray-400 dark:text-gray-500"}">
            ${item.value}
          </p>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function displayExperience(experience) {
  const timelineContainer = document.getElementById("experienceTimeline");

  // Update summary stats
  document.getElementById("totalYears").textContent =
    experience.total_years || 0;
  document.getElementById("totalPositions").textContent =
    experience.total_positions || experience.positions || 0;

  // Determine experience level
  const totalYears = experience.total_years || 0;
  let level = "Entry Level";
  if (totalYears >= 10) level = "Senior";
  else if (totalYears >= 5) level = "Mid-Level";
  else if (totalYears >= 2) level = "Junior";
  else if (totalYears >= 1) level = "Entry Level";
  else level = "Fresher";

  document.getElementById("expLevel").textContent = level;

  // Display experience items
  if (
    !experience.experiences ||
    !Array.isArray(experience.experiences) ||
    experience.experiences.length === 0
  ) {
    timelineContainer.innerHTML =
      '<p class="text-gray-500 dark:text-gray-400">No work experience data available</p>';
    return;
  }

  let html = "";
  experience.experiences.forEach((exp) => {
    const isInternship = exp.is_internship || exp.type === "Internship";
    const typeColor = isInternship ? "yellow" : "blue";
    const typeBg = isInternship
      ? "bg-yellow-100 dark:bg-yellow-900"
      : "bg-blue-100 dark:bg-blue-900";
    const typeText = isInternship
      ? "text-yellow-700 dark:text-yellow-300"
      : "text-blue-700 dark:text-blue-300";

    html += `
      <div class="timeline-item">
        <div class="mb-2">
          <div class="flex items-start justify-between flex-wrap gap-2">
            <div>
              <h4 class="text-lg font-semibold text-gray-800 dark:text-white">${exp.title || "Position"}</h4>
              <p class="text-sm text-gray-600 dark:text-gray-400">${exp.company || "Company"}</p>
            </div>
            <span class="text-xs px-3 py-1 rounded-full ${typeBg} ${typeText} font-medium">
              ${exp.type || (isInternship ? "Internship" : "Full-time")}
            </span>
          </div>
          <div class="mt-2 flex items-center text-sm text-gray-500 dark:text-gray-400">
            <i class="far fa-calendar mr-2"></i>
            ${exp.dates || "Dates not specified"}
            <span class="mx-2">•</span>
            <span class="font-medium">${exp.years || 0} years</span>
          </div>
          ${exp.description ? `<p class="mt-2 text-sm text-gray-600 dark:text-gray-300">${exp.description}</p>` : ""}
        </div>
      </div>
    `;
  });

  timelineContainer.innerHTML = html;
}

function displaySkills(skills, jobRole, roleConfidence) {
  const container = document.getElementById("skillsSection");

  if (
    !skills ||
    !skills.technical ||
    Object.keys(skills.technical).length === 0
  ) {
    container.innerHTML =
      '<p class="text-gray-500 dark:text-gray-400">No skills data available</p>';
    return;
  }

  let html = "";

  Object.entries(skills.technical).forEach(([category, skillList]) => {
    const categoryIcons = {
      programming: "code",
      web: "globe",
      database: "database",
      cloud: "cloud",
      cloud_devops: "cloud",
      devops: "server",
      data_science: "chart-line",
      frameworks: "layer-group",
      testing: "vial",
      mobile: "mobile-alt",
      design: "palette",
      tools: "tools",
    };

    const icon = categoryIcons[category] || "circle";
    const displayCategory = category
      .split("_")
      .map((word) => word.charAt(0).toUpperCase() + word.slice(1))
      .join(" ");

    html += `
      <div>
        <h4 class="text-lg font-semibold text-gray-700 dark:text-gray-200 mb-3 flex items-center">
          <i class="fas fa-${icon} text-primary mr-2"></i>
          ${displayCategory}
          <span class="ml-2 text-sm text-gray-500 dark:text-gray-400">(${skillList.length})</span>
        </h4>
        <div class="flex flex-wrap gap-2">
          ${skillList.map((skill) => `<span class="skill-badge">${skill}</span>`).join("")}
        </div>
      </div>
    `;
  });

  container.innerHTML = html;

  // Display predicted role
  if (jobRole) {
    const roleEl = document.getElementById("predictedRole");
    const confEl = document.getElementById("roleConfidence");

    if (roleEl) roleEl.textContent = jobRole || "Unknown";
    if (confEl) confEl.textContent = (roleConfidence || 0) + "%";
  }
}

function displayAdvantagesDisadvantages(advantages, disadvantages) {
  const advContainer = document.getElementById("advantagesSection");
  const disadvContainer = document.getElementById("disadvantagesSection");

  // Advantages
  if (!advantages || (Array.isArray(advantages) && advantages.length === 0)) {
    advContainer.innerHTML =
      '<p class="text-gray-500 dark:text-gray-400">No specific strengths identified</p>';
  } else {
    let html = '<ul class="space-y-2">';

    if (Array.isArray(advantages)) {
      advantages.forEach((item) => {
        html += `
          <li class="text-sm text-gray-600 dark:text-gray-400 flex items-start">
            <i class="fas fa-check-circle text-green-500 mr-2 mt-1"></i>
            <span>${item}</span>
          </li>
        `;
      });
    }

    html += "</ul>";
    advContainer.innerHTML = html;
  }

  // Disadvantages
  if (
    !disadvantages ||
    (Array.isArray(disadvantages) && disadvantages.length === 0)
  ) {
    disadvContainer.innerHTML =
      '<p class="text-gray-500 dark:text-gray-400">No areas for improvement identified</p>';
  } else {
    let html = '<ul class="space-y-2">';

    if (Array.isArray(disadvantages)) {
      disadvantages.forEach((item) => {
        html += `
          <li class="text-sm text-gray-600 dark:text-gray-400 flex items-start">
            <i class="fas fa-exclamation-triangle text-orange-500 mr-2 mt-1"></i>
            <span>${item}</span>
          </li>
        `;
      });
    }

    html += "</ul>";
    disadvContainer.innerHTML = html;
  }
}

function displaySuggestions(suggestions) {
  const container = document.getElementById("suggestionsSection");

  if (!suggestions || suggestions.length === 0) {
    container.innerHTML =
      '<p class="text-gray-500 dark:text-gray-400">No specific suggestions at this time</p>';
    return;
  }

  let html = "";

  suggestions.forEach((suggestion) => {
    const parts = suggestion.match(
      /^([\u{1F300}-\u{1F9FF}]|\u{2700}-\u{27BF}|\u{2B50}|[🎯💼🛠️🔗📁✍️📊📝⚠️])\s*(.+)$/u,
    );
    const emoji = parts ? parts[1] : "💡";
    const text = parts ? parts[2] : suggestion;

    let priority = "Medium";
    let color = "blue";

    if (
      text.toLowerCase().includes("missing") ||
      text.toLowerCase().includes("no ") ||
      text.toLowerCase().includes("limited")
    ) {
      priority = "High";
      color = "red";
    } else if (
      text.toLowerCase().includes("add") ||
      text.toLowerCase().includes("include")
    ) {
      priority = "Medium";
      color = "yellow";
    } else {
      priority = "Low";
      color = "blue";
    }

    html += `
      <div class="p-4 bg-white dark:bg-gray-800 border-l-4 border-${color}-500 rounded-r-lg shadow-sm hover:shadow-md transition-shadow">
        <div class="flex items-start space-x-3">
          <span class="text-2xl">${emoji}</span>
          <div class="flex-1">
            <div class="flex items-center justify-between mb-2">
              <span class="text-xs px-2 py-1 rounded-full bg-${color}-100 dark:bg-${color}-900 text-${color}-700 dark:text-${color}-300 font-medium">
                ${priority} Priority
              </span>
            </div>
            <p class="text-sm text-gray-700 dark:text-gray-300">${text}</p>
          </div>
        </div>
      </div>
    `;
  });

  container.innerHTML = html;
}

function displayError(message) {
  const container = document.getElementById("errorSection");
  if (container) container.innerHTML = `<p class="text-red-500">${message}</p>`;
}

// Function to view resume in new tab
function viewResume(viewUrl) {
  if (viewUrl) {
    // Open in new tab
    window.open(viewUrl, "_blank");
  } else {
    showError("Resume view URL not available");
  }
}

// Function to download resume
function downloadResume(downloadUrl, filename) {
  if (downloadUrl) {
    // Create a temporary link and trigger download
    const link = document.createElement("a");
    link.href = downloadUrl;
    link.download = filename || "resume.pdf";
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    // Show success message
    showSuccess("Resume download started!");
  } else {
    showError("Resume download URL not available");
  }
}

// Helper function to show success message
function showSuccess(message) {
  const toast = document.createElement("div");
  toast.className =
    "fixed bottom-4 right-4 bg-green-500 text-white px-6 py-3 rounded-lg shadow-lg z-50 fade-in";
  toast.innerHTML = `
    <div class="flex items-center space-x-2">
      <i class="fas fa-check-circle"></i>
      <span>${message}</span>
    </div>
  `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.style.opacity = "0";
    setTimeout(() => toast.remove(), 300);
  }, 3000);
}

// =====================================================================
// COVER LETTER GENERATOR
// =====================================================================

// Analysis data is stored inside displayResults directly — no wrapper needed

async function generateCoverLetter() {
  const jdUrl = (document.getElementById("clJdUrl")?.value || "").trim();
  const btn = document.getElementById("clGenerateBtn");
  const statusBar = document.getElementById("clStatusBar");
  const errorBar = document.getElementById("clErrorBar");
  const wrapper = document.getElementById("clLetterWrapper");
  const analysis = window._clAnalysisData || analysisData;

  if (!analysis) {
    showClError("No resume analysis found. Please analyze your resume first.");
    return;
  }

  // Reset UI state
  statusBar.classList.add("hidden");
  errorBar.classList.add("hidden");
  wrapper.classList.add("hidden");

  // Show loading state on button
  btn.disabled = true;
  btn.innerHTML = '<span class="cl-spinner"></span> Generating...';

  try {
    const res = await fetch("/generate-cover-letter", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ analysis, jd_url: jdUrl, jd_text: "" }),
    });

    const result = await res.json();

    if (!res.ok || !result.success) {
      throw new Error(result.error || "Generation failed");
    }

    // Populate letter
    document.getElementById("clLetterText").value = result.cover_letter;

    // Populate status bar
    document.getElementById("clJobTitle").textContent =
      result.jd_title || "the position";
    document.getElementById("clCompanyName").textContent =
      result.jd_company || "the company";

    const skillsContainer = document.getElementById("clMatchedSkills");
    if (result.matched_skills && result.matched_skills.length > 0) {
      skillsContainer.innerHTML =
        '<span class="text-xs text-green-600 dark:text-green-400 font-medium mr-1">Skills matched:</span>' +
        result.matched_skills
          .map(
            (s) =>
              `<span class="cl-skill-match"><i class="fas fa-check" style="font-size:9px"></i>${s}</span>`,
          )
          .join("");
    } else {
      skillsContainer.innerHTML =
        '<span class="text-xs text-gray-500">General cover letter generated based on your resume.</span>';
    }

    // Show UI
    statusBar.classList.remove("hidden");
    wrapper.classList.remove("hidden");

    // Smooth scroll to letter
    wrapper.scrollIntoView({ behavior: "smooth", block: "start" });

    // Toast
    showSuccess("Cover letter generated successfully!");
  } catch (err) {
    showClError(
      err.message || "Failed to generate cover letter. Please try again.",
    );
    console.error("Cover letter error:", err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-bolt mr-2"></i>Generate Cover Letter';
  }
}

function showClError(msg) {
  const errorBar = document.getElementById("clErrorBar");
  document.getElementById("clErrorMsg").textContent = msg;
  errorBar.classList.remove("hidden");
  errorBar.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function clCopyLetter() {
  const text = document.getElementById("clLetterText")?.value;
  if (!text) return;
  navigator.clipboard
    .writeText(text)
    .then(() => {
      showSuccess("Cover letter copied to clipboard!");
    })
    .catch(() => {
      // Fallback for older browsers
      document.getElementById("clLetterText").select();
      document.execCommand("copy");
      showSuccess("Cover letter copied!");
    });
}

function clDownloadLetter() {
  const text = document.getElementById("clLetterText")?.value || "";
  const company =
    document.getElementById("clCompanyName")?.textContent || "Company";
  const name = (
    window._clAnalysisData?.personal_details?.name || "Cover_Letter"
  ).replace(/\s+/g, "_");
  const filename = `${name}_Cover_Letter_${company.replace(/\s+/g, "_")}.txt`;

  const blob = new Blob([text], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showSuccess("Cover letter downloaded!");
}

function clRegenerateLetter() {
  // Clear URL and regenerate (general format)
  generateCoverLetter();
}

// =====================================================================
// COMPANY SUGGESTIONS
// =====================================================================

async function fetchCompanySuggestions(jobRole, experienceLevel, totalYears) {
  try {
    const res = await fetch("/suggest-companies", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        job_role: jobRole,
        experience_level: experienceLevel,
        total_years: totalYears,
      }),
    });

    if (!res.ok) throw new Error("Server error");
    const data = await res.json();
    if (!data.success) throw new Error(data.error || "Failed");

    renderCompanyCards(data);
  } catch (err) {
    console.error("Company suggestions error:", err);
    document.getElementById("coGrid").innerHTML = `
      <div class="col-span-3 text-center py-8 text-gray-400 dark:text-gray-500">
        <i class="fas fa-exclamation-circle text-3xl mb-3 block"></i>
        Could not load company suggestions. Please refresh and try again.
      </div>`;
    document.getElementById("coRoleLine").textContent = "";
  }
}

function renderCompanyCards(data) {
  const grid = document.getElementById("coGrid");
  const badge = document.getElementById("coLevelBadge");
  const levelTxt = document.getElementById("coLevelText");
  const roleLine = document.getElementById("coRoleLine");
  const isDark = document.documentElement.classList.contains("dark");

  // Level badge
  levelTxt.textContent = data.level;
  badge.classList.remove("hidden");

  // Role line
  roleLine.textContent = `Showing ${data.companies.length} curated companies for ${data.job_role} — ${data.level}`;

  if (!data.companies || data.companies.length === 0) {
    grid.innerHTML = `
      <div class="col-span-3 text-center py-8 text-gray-400 dark:text-gray-500">
        <i class="fas fa-search text-3xl mb-3 block"></i>
        No specific suggestions found for this role yet.
      </div>`;
    return;
  }

  // Type → CSS class map
  const typeClass = (type) => {
    const map = {
      Product: "co-type-Product",
      Service: "co-type-Service",
      Startup: "co-type-Startup",
      MNC: "co-type-MNC",
      Consulting: "co-type-Consulting",
      Analytics: "co-type-Analytics",
      Agency: "co-type-Agency",
      BFSI: "co-type-BFSI",
    };
    return map[type] || "co-type-Product";
  };

  // Company initial avatar colour (cycle through palette)
  const avatarColors = [
    "linear-gradient(135deg,#667eea,#764ba2)",
    "linear-gradient(135deg,#10b981,#3b82f6)",
    "linear-gradient(135deg,#f59e0b,#ef4444)",
    "linear-gradient(135deg,#8b5cf6,#ec4899)",
    "linear-gradient(135deg,#14b8a6,#6366f1)",
    "linear-gradient(135deg,#f97316,#eab308)",
  ];

  grid.innerHTML = data.companies
    .map((c, i) => {
      const initial = (c.name || "?")[0].toUpperCase();
      const avatarBg = avatarColors[i % avatarColors.length];
      const tagsHtml = (c.tags || [])
        .slice(0, 3)
        .map((t) => `<span class="co-tag">${t}</span>`)
        .join("");
      const typeHtml = `<span class="co-type-badge ${typeClass(c.type)}">${c.type}</span>`;

      return `
      <div class="company-card p-5 flex flex-col gap-3">
        <!-- Top row: avatar + name + type -->
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 rounded-xl flex items-center justify-center flex-shrink-0 text-white font-bold text-lg"
               style="background:${avatarBg}">${initial}</div>
          <div class="flex-1 min-w-0">
            <div class="font-bold text-gray-800 dark:text-white text-sm leading-tight truncate">${c.name}</div>
            <div class="mt-0.5">${typeHtml}</div>
          </div>
        </div>

        <!-- Tags row -->
        <div class="flex flex-wrap gap-1.5">
          ${tagsHtml}
        </div>

        <!-- Salary + Apply -->
        <div class="flex items-center justify-between mt-auto pt-1">
          <span class="co-salary">${c.salary_band}</span>
          <a href="${c.careers_url}" target="_blank" rel="noopener noreferrer"
             class="co-apply-btn text-white font-bold px-4 py-1.5 rounded-lg flex items-center gap-1.5">
            <i class="fas fa-external-link-alt text-xs"></i> Apply Now
          </a>
        </div>
      </div>`;
    })
    .join("");
}

// =====================================================================
// LATEX RESUME GENERATOR
// =====================================================================

let _ltxCode = "";
let _ltxFilename = "Resume.tex";

async function generateLatex() {
  const btn = document.getElementById("ltxGenerateBtn");
  const errorBar = document.getElementById("ltxErrorBar");
  const wrapper = document.getElementById("ltxCodeWrapper");
  const analysis = window._clAnalysisData || analysisData;

  if (!analysis) {
    showLtxError("No resume analysis found. Please analyze your resume first.");
    return;
  }

  // Reset
  errorBar.classList.add("hidden");
  wrapper.classList.add("hidden");
  btn.disabled = true;
  btn.innerHTML = '<span class="cl-spinner"></span> Generating LaTeX...';

  try {
    const res = await fetch("/generate-latex", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ analysis }),
    });

    const data = await res.json();
    if (!res.ok || !data.success)
      throw new Error(data.error || "Generation failed");

    _ltxCode = data.latex_code;
    _ltxFilename = data.filename || "Resume.tex";

    // Update filename labels
    document.getElementById("ltxFilename").textContent = _ltxFilename;
    document.getElementById("ltxModalFilename").textContent = _ltxFilename;

    // Render syntax-highlighted preview
    document.getElementById("ltxCodeDisplay").innerHTML =
      ltxHighlight(_ltxCode);

    // Populate modal textarea (plain, editable)
    document.getElementById("ltxModalCode").value = _ltxCode;

    wrapper.classList.remove("hidden");
    wrapper.scrollIntoView({ behavior: "smooth", block: "start" });
    showSuccess("LaTeX resume generated! Ready to use in Overleaf.");
  } catch (err) {
    showLtxError(err.message || "Failed to generate LaTeX. Please try again.");
    console.error("LaTeX error:", err);
  } finally {
    btn.disabled = false;
    btn.innerHTML = '<i class="fas fa-magic"></i> Generate LaTeX Code';
  }
}

// Basic syntax highlighting for LaTeX
function ltxHighlight(code) {
  const escaped = code
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  return (
    escaped
      // Comments
      .replace(
        /(%%[^\n]*)/g,
        '<span style="color:#6b7280;font-style:italic">$1</span>',
      )
      // Commands: \something
      .replace(/(\\[a-zA-Z@]+)/g, '<span style="color:#c4b5fd">$1</span>')
      // Curly braces
      .replace(/([{}])/g, '<span style="color:#fbbf24">$1</span>')
      // Square brackets
      .replace(/(\[[^\]]*\])/g, '<span style="color:#6ee7b7">$1</span>')
  );
}

function showLtxError(msg) {
  const bar = document.getElementById("ltxErrorBar");
  document.getElementById("ltxErrorMsg").textContent = msg;
  bar.classList.remove("hidden");
  bar.scrollIntoView({ behavior: "smooth", block: "nearest" });
}

function ltxCopy() {
  // Prefer modal textarea value (in case user edited it)
  const code = document.getElementById("ltxModalCode").value || _ltxCode;
  if (!code) return;
  navigator.clipboard
    .writeText(code)
    .then(() => showSuccess("LaTeX code copied to clipboard!"))
    .catch(() => {
      const ta = document.getElementById("ltxModalCode");
      ta.select();
      document.execCommand("copy");
      showSuccess("LaTeX code copied!");
    });
}

function ltxDownload() {
  const code = document.getElementById("ltxModalCode").value || _ltxCode;
  if (!code) return;
  const blob = new Blob([code], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const a = Object.assign(document.createElement("a"), {
    href: url,
    download: _ltxFilename,
  });
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showSuccess(`${_ltxFilename} downloaded!`);
}

function ltxOpenModal() {
  document.getElementById("ltxModal").classList.remove("hidden");
  document.body.style.overflow = "hidden";
}

function ltxCloseModal() {
  // Sync any edits back to preview before closing
  const edited = document.getElementById("ltxModalCode").value;
  if (edited) {
    _ltxCode = edited;
    document.getElementById("ltxCodeDisplay").innerHTML = ltxHighlight(edited);
  }
  document.getElementById("ltxModal").classList.add("hidden");
  document.body.style.overflow = "";
}

// Close modal on backdrop click
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("ltxModal")?.addEventListener("click", (e) => {
    if (e.target.id === "ltxModal") ltxCloseModal();
  });
});
