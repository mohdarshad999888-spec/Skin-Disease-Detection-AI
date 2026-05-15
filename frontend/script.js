async function uploadImage() {

  // =========================
  // START
  // =========================

  console.log("UPLOAD STARTED");

  // =========================
  // FILE INPUT
  // =========================

  const fileInput =
    document.getElementById("imageInput");

  const file =
    fileInput.files[0];

  // =========================
  // VALIDATION
  // =========================

  if (!file) {

    alert(
      "Please upload image first"
    );

    return;

  }

  // =========================
  // ELEMENTS
  // =========================

  const preview =
    document.getElementById("preview");

  const status =
    document.getElementById("status");

  const progress =
    document.getElementById("progress");

  const disease =
    document.getElementById("disease");

  const confidenceText =
    document.getElementById("confidence");

  const heatmap =
    document.getElementById("heatmap");

  // =========================
  // IMAGE PREVIEW
  // =========================

  preview.src =
    URL.createObjectURL(file);

  preview.style.display =
    "block";

  // =========================
  // RESET UI
  // =========================

  disease.innerText = "";

  confidenceText.innerText = "";

  heatmap.src = "";

  heatmap.style.display =
    "none";

  // =========================
  // AI LOADING ANIMATION
  // =========================

  status.innerText =
    "Uploading image...";

  progress.style.width =
    "20%";

  progress.classList.add(
    "loading"
  );

  animateElement(
    ".analysis-card"
  );

  setTimeout(() => {

    status.innerText =
      "Analyzing skin texture...";

    progress.style.width =
      "45%";

  }, 700);

  setTimeout(() => {

    status.innerText =
      "Generating AI prediction...";

    progress.style.width =
      "70%";

  }, 1400);

  // =========================
  // FORM DATA
  // =========================

  const formData =
    new FormData();

  formData.append(
    "file",
    file
  );

  try {

    console.log(
      "Sending request..."
    );

    // =========================
    // FETCH API
    // =========================

    const response =
      await fetch(
        "http://127.0.0.1:5000/predict",
        {
          method: "POST",
          body: formData
        }
      );

    // =========================
    // RESPONSE CHECK
    // =========================

    if (!response.ok) {

      throw new Error(
        "Backend Server Error"
      );

    }

    // =========================
    // JSON DATA
    // =========================

    const data =
      await response.json();

    console.log(
      "Backend Response:",
      data
    );

    // =========================
    // COMPLETE
    // =========================

    progress.style.width =
      "100%";

    progress.classList.remove(
      "loading"
    );

    status.innerText =
      "AI Analysis Complete";

    // =========================
    // DISEASE RESULT
    // =========================

    disease.innerText =
      data.disease ||
      "Unknown Disease";

    animateElement(
      "#disease"
    );

    // =========================
    // CONFIDENCE
    // =========================

    const confidence =
      Math.round(
        Number(
          data.confidence
        ) * 100
      );

    confidenceText.innerText =
      "AI Confidence: "
      + confidence + "%";

    animateElement(
      "#confidence"
    );

    // =========================
    // HEATMAP
    // =========================

    if (data.heatmap) {

      heatmap.src =
        "http://127.0.0.1:5000/"
        + data.heatmap;

      heatmap.style.display =
        "block";

      animateElement(
        "#heatmap"
      );

    }

    // =========================
    // GRAPH
    // =========================

    const bar1 =
      confidence;

    const bar2 =
      Math.max(
        confidence - 20,
        20
      );

    const bar3 =
      Math.max(
        confidence - 40,
        10
      );

    document
      .getElementById("bar1")
      .style.height =
      bar1 + "px";

    document
      .getElementById("bar2")
      .style.height =
      bar2 + "px";

    document
      .getElementById("bar3")
      .style.height =
      bar3 + "px";

    animateBars();

    console.log(
      "GRAPH UPDATED"
    );

  }

  // =========================
  // ERROR
  // =========================

  catch (error) {

    console.error(
      "FULL ERROR:",
      error
    );

    status.innerText =
      "Backend Connection Failed";

    progress.style.width =
      "0%";

    progress.classList.remove(
      "loading"
    );

    disease.innerText =
      "Connection Error";

    confidenceText.innerText =
      "";

    heatmap.style.display =
      "none";

    alert(
      "Unable to connect backend server"
    );

  }

}

// =========================
// LOAD HISTORY
// =========================

async function loadHistory(){

  showSection(
    "historySection"
  );

  setActiveMenu(
    "historyMenu"
  );

  const historyStatus =
    document.getElementById(
      "historyStatus"
    );

  const historyList =
    document.getElementById(
      "historyList"
    );

  historyStatus.innerText =
    "Loading scan history...";

  historyList.innerHTML =
    "";

  try{

    const response =
      await fetch(
        "http://127.0.0.1:5000/history"
      );

    if (!response.ok) {

      throw new Error(
        "Unable to load history"
      );

    }

    const data =
      await response.json();

    if (!data.length) {

      historyStatus.innerText =
        "No scan history found.";

      return;

    }

    historyStatus.innerText =
      "";

    data.forEach(item => {

      const historyItem =
        document.createElement(
          "div"
        );

      historyItem.className =
        "next";

      const diseaseTitle =
        document.createElement(
          "h4"
        );

      diseaseTitle.innerText =
        item.disease ||
        "Unknown Disease";

      const confidence =
        document.createElement(
          "p"
        );

      confidence.innerText =
        "Confidence: "
        + (item.confidence ?? "N/A")
        + "%";

      const date =
        document.createElement(
          "p"
        );

      date.innerText =
        "Date: "
        + (item.date || "N/A");

      const image =
        document.createElement(
          "p"
        );

      image.innerText =
        "Image: "
        + (item.image || "N/A");

      historyItem.append(
        diseaseTitle,
        confidence,
        date,
        image
      );

      historyList.appendChild(
        historyItem
      );

      animateElement(
        historyItem
      );

    });

  }

  catch(error){

    historyStatus.innerText =
      "Unable to load history";

    historyList.innerHTML =
      "";

  }

}

// =========================
// DASHBOARD
// =========================

function goDashboard(){

  showSection(
    "dashboardSection"
  );

  setActiveMenu(
    "dashboardMenu"
  );

}

// =========================
// PAGE ANIMATIONS
// =========================

document.addEventListener(
  "DOMContentLoaded",
  () => {

    runIntroAnimations();
    wireInteractiveMotion();

  }
);

function runIntroAnimations(){

  if (!window.gsap) {

    return;

  }

  gsap.from(
    ".sidebar",
    {
      x: -38,
      opacity: 0,
      duration: 0.8,
      ease: "power3.out"
    }
  );

  gsap.from(
    ".top-header",
    {
      y: 26,
      opacity: 0,
      duration: 0.75,
      delay: 0.12,
      ease: "power3.out"
    }
  );

  gsap.from(
    ".card",
    {
      y: 34,
      opacity: 0,
      duration: 0.7,
      stagger: 0.12,
      delay: 0.25,
      ease: "power3.out"
    }
  );

}

function wireInteractiveMotion(){

  const cards =
    document.querySelectorAll(
      ".card"
    );

  cards.forEach(card => {

    card.addEventListener(
      "mousemove",
      event => {

        const bounds =
          card.getBoundingClientRect();

        const rotateY =
          ((event.clientX - bounds.left) / bounds.width - 0.5) * 4;

        const rotateX =
          ((event.clientY - bounds.top) / bounds.height - 0.5) * -4;

        card.style.transform =
          "translateY(-8px) rotateX("
          + rotateX
          + "deg) rotateY("
          + rotateY
          + "deg)";

      }
    );

    card.addEventListener(
      "mouseleave",
      () => {

        card.style.transform =
          "";

      }
    );

  });

}

function animateElement(selector){

  if (!window.gsap) {

    return;

  }

  gsap.fromTo(
    selector,
    {
      y: 16,
      opacity: 0,
      scale: 0.98
    },
    {
      y: 0,
      opacity: 1,
      scale: 1,
      duration: 0.45,
      ease: "power3.out"
    }
  );

}

function animateBars(){

  if (!window.gsap) {

    return;

  }

  gsap.from(
    ".bar",
    {
      height: 8,
      duration: 0.72,
      stagger: 0.08,
      ease: "power3.out"
    }
  );

}

// =========================
// SECTION SWITCHER
// =========================

function showSection(sectionId){

  const sections = [
    "dashboardSection",
    "historySection"
  ];

  sections.forEach(id => {

    const section =
      document.getElementById(id);

    if (section) {

      section.style.display =
        id === sectionId
          ? "grid"
          : "none";

      if (id === sectionId) {

        animateElement(
          section
        );

        section.scrollIntoView({
          behavior: "smooth",
          block: "start"
        });

      }

    }

  });

}

// =========================
// ACTIVE MENU
// =========================

function setActiveMenu(menuId){

  const menuItems =
    document.querySelectorAll(
      ".menu li"
    );

  menuItems.forEach(item => {

    item.classList.remove(
      "active"
    );

  });

  const activeMenu =
    document.getElementById(
      menuId
    );

  if (activeMenu) {

    activeMenu.classList.add(
      "active"
    );

  }

}

// =========================
// AI RESOURCES
// =========================

function showResources(){

  alert(
    "AI Skin Disease Resources Coming Soon"
  );

}

// =========================
// DOCTORS
// =========================

function showDoctors(){

  alert(
    "Doctors Panel Coming Soon"
  );

}

// =========================
// PROFILE
// =========================

function showProfile(){

  alert(
    "User Profile Coming Soon"
  );

}
