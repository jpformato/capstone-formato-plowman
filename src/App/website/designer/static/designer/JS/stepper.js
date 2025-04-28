// DOM Elements
const circles = document.querySelectorAll(".circle");
const progressBar = document.querySelector(".indicator");
const progressData = JSON.parse(document.getElementById('progress-json').textContent);

// Modal logic
const modal = document.getElementById("modal");
const closeBtn = document.querySelector(".close");
const form = document.getElementById("stepForm");

let currentStep = 1;
let activeStepIndex = null;

// Set initial state from progress data 
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Track state: 'not-started' | 'started' | 'completed'
const stepStates = Array.from(circles).map(() => "not-started");

const updateStepUI = () => {
    let lastCompletedIndex = -1;

    circles.forEach((circle, index) => {
        const icon = circle.querySelector(".step-icon");
        circle.classList.remove("active", "started");
        icon.textContent = "";

        // Clear previous date display
        const existingLabel = circle.querySelector(".step-dates");
        if (existingLabel) existingLabel.remove();

        // Get stored values
        const startDate = circle.dataset.startDate || "";
        const completedDate = circle.dataset.completedDate || "";

        // Create display
        let dateHTML = "";
        if (startDate) dateHTML += `<div class="date-label">Start: ${startDate}</div>`;
        if (completedDate) dateHTML += `<div class="date-label">Done: ${completedDate}</div>`;

        if (dateHTML) {
            const dateContainer = document.createElement("div");
            dateContainer.className = "step-dates";
            dateContainer.innerHTML = dateHTML;
            circle.appendChild(dateContainer);
        }

        if (stepStates[index] === "completed") {
            circle.classList.add("active");
            icon.textContent = "✓";
            const nextIndex = index + 0.6;
            const maxIndex = circles.length - 1;
            lastCompletedIndex = Math.min(nextIndex, maxIndex);
        } else if (stepStates[index] === "started") {
            circle.classList.add("started");
            icon.textContent = "...";
            if (lastCompletedIndex < index) lastCompletedIndex = index;
        }
    });

    const progressPercent = (lastCompletedIndex / (circles.length - 1)) * 100;
    progressBar.style.width = `${Math.max(progressPercent, 0)}%`;
};

circles.forEach((circle, index) => {
    circle.style.cursor = "pointer";
    circle.addEventListener("click", () => {
        if (index > 0 && stepStates[index - 1] !== "completed") {
            alert(`You must complete step "${circles[index - 1].innerText.trim()}" before starting this one.`);
            return;
        }

        activeStepIndex = index;
        const stepName = circle.querySelector(".step-number").textContent.trim();
        const progress = progressData[stepName];

        // Pre-fill modal fields if data exists
        document.getElementById("dateStarted").value = progress?.start_date || "";
        document.getElementById("dateCompleted").value = progress?.end_date || "";
        document.getElementById("notes").value = progress?.notes || "";

        modal.style.display = "block";
    });
});

closeBtn.onclick = function () {
    modal.style.display = "none";
};

window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = "none";
    }
};

// Handle form submission
form.onsubmit = function (e) {
    e.preventDefault();

    const started = document.getElementById("dateStarted").value.trim();
    const completed = document.getElementById("dateCompleted").value.trim();
    const notes = document.getElementById("notes").value.trim();

    const dateRegex = /^\d{2}\/\d{2}\/\d{2}$/;

    let validStarted = false;
    let validCompleted = false;

    if (started) {
        if (!dateRegex.test(started) || !isValidDate(started)) {
            alert("Please enter a valid start date in the format MM/DD/YY.");
            return;
        }
        validStarted = true;
    }

    if (completed) {
        if (!dateRegex.test(completed) || !isValidDate(completed)) {
            alert("Please enter a valid completion date in the format MM/DD/YY.");
            return;
        }
        validCompleted = true;
    }

    if (validStarted && validCompleted) {
        const startDate = parseDate(started);
        const completedDate = parseDate(completed);
        if (completedDate < startDate) {
            alert("Completion date cannot be earlier than the start date.");
            return;
        }
    }

    if (!validStarted && !validCompleted && !notes) {
        alert("Please enter at least one field to update.");
        return;
    }

    // Update state
    if (validCompleted) {
        stepStates[activeStepIndex] = "completed";
    } else if (validStarted) {
        stepStates[activeStepIndex] = "started";
    }

    // Store date info on circle
    const circle = circles[activeStepIndex];
    if (validStarted) circle.dataset.startDate = started;
    if (validCompleted) circle.dataset.completedDate = completed;

    console.log(`Step ${activeStepIndex + 1} updated:`, {
        started,
        completed,
        notes,
        status: stepStates[activeStepIndex]
    });

    fetch("/progress/update/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")  // needed unless @csrf_exempt
        },
        body: JSON.stringify({
            project_id: PROJECT_ID,
            step_name: document.querySelectorAll(".step-number")[activeStepIndex].textContent.trim(),
            start_date: validStarted ? started : null,
            end_date: validCompleted ? completed : null,
            notes: notes
        }),
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            console.error("Failed to update:", data.error);
        } else {
            console.log("Progress saved.");
        }
    });    

    // Email Creation Logic
    const stepName = document.querySelectorAll(".step-number")[activeStepIndex].textContent.trim();

    // Create email body based on the update to project
    let updateMessage = "";

    // Only show what actually changed
    const startedChanged = started !== progressData[stepName]?.start_date;
    const completedChanged = completed !== progressData[stepName]?.end_date;
    const notesChanged = notes && notes !== (progressData[stepName]?.notes);
    
    if (startedChanged) {
        updateMessage += `Step "${stepName}" was started on ${started}.`;
    }
    
    if (completedChanged) {
        if (updateMessage) updateMessage += "\n\n";
        updateMessage += `Step "${stepName}" was completed on ${completed}.`;
    }
    
    if (notesChanged) {
        if (updateMessage) updateMessage += "\n\n";
        updateMessage += `Notes for step "${stepName}": ${notes}`;
    }

    // Send the Email 
    emailjs.send("service_h71srho", "template_zxuz93z", {
        email: CUSTOMER_EMAIL,  // The person who should receive the email
        reply_to: "cmplowman@loyola.edu",  // Shows up when they click Reply
        project_id: PROJECT_ID,
        update_message: updateMessage,     
    })
    .then((response) => {
        console.log("Email sent:", response.status, response.text);
    })
    .catch((error) => {
        console.error("EmailJS error:", error);
    }); 
    
    // Update progressData for immediate UI sync
    progressData[stepName] = {
        start_date: started,
        end_date: completed,         
        notes: notes                 
    };
    
    modal.style.display = "none";
    updateStepUI();
};

// Auto-format MM/DD/YY input
function formatDateInput(input) {
    input.addEventListener("input", () => {
        let digits = input.value.replace(/[^\d]/g, "");

        if (digits.length > 6) digits = digits.slice(0, 6);

        let formatted = "";
        if (digits.length >= 2) {
            formatted += digits.slice(0, 2) + "/";
        } else {
            formatted += digits;
        }

        if (digits.length >= 4) {
            formatted += digits.slice(2, 4) + "/";
        } else if (digits.length > 2) {
            formatted += digits.slice(2);
        }

        if (digits.length > 4) {
            formatted += digits.slice(4);
        }

        input.value = formatted;
    });

    input.addEventListener("keydown", (e) => {
        const allowedKeys = ["Backspace", "ArrowLeft", "ArrowRight", "Tab", "Delete"];
        if (allowedKeys.includes(e.key)) return;

        if (input.value.length >= 8) {
            e.preventDefault();
        }
    });
}
formatDateInput(document.getElementById("dateStarted"));
formatDateInput(document.getElementById("dateCompleted"));

// Validate MM/DD/YY
function isValidDate(dateStr) {
    const [mm, dd, yy] = dateStr.split("/").map(Number);

    if (mm < 1 || mm > 12 || dd < 1 || dd > 31) return false;
    if (mm === 2 && dd > 29) return false;
    if ([4, 6, 9, 11].includes(mm) && dd > 30) return false;

    const fullYear = 2000 + yy;
    const dateObj = new Date(fullYear, mm - 1, dd);

    return (
        dateObj.getFullYear() === fullYear &&
        dateObj.getMonth() === mm - 1 &&
        dateObj.getDate() === dd
    );
}

// Parse MM/DD/YY into Date object
function parseDate(dateStr) {
    const [mm, dd, yy] = dateStr.split("/").map(Number);
    return new Date(2000 + yy, mm - 1, dd);
}

circles.forEach((circle, index) => {
    const stepName = circle.querySelector(".step-number").textContent.trim();
    const progress = progressData[stepName];

    if (progress) {
        if (progress.start_date) {
            stepStates[index] = "started";
            circle.dataset.startDate = progress.start_date;
        }

        if (progress.end_date) {
            stepStates[index] = "completed";
            circle.dataset.completedDate = progress.end_date;
        }
    }
});

// Initial render
updateStepUI();
