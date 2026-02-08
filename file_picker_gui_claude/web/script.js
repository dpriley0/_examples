/**
 * app.js — Frontend logic for the New Project workflow.
 *
 * THE ASYNC FLOW (this is the key concept):
 * ==========================================
 * 1. User clicks "New Project" button
 * 2. JS calls eel.browse_for_model_directory()  → Python opens OS dialog
 * 3. Python returns {success, path, project_name} → JS receives it
 * 4. JS calls eel.create_new_project(path, name) → Python creates ProjectIdentity
 * 5. Python returns {success, project: {...}}     → JS updates the DOM
 *
 * WHY async/await?
 *   Every eel.python_function()() call crosses a process boundary
 *   (JS → Python → JS). This takes real time (the user is picking a
 *   folder!), so we use async/await to keep the GUI responsive.
 *
 * THE DOUBLE-PARENTHESES PATTERN:
 *   eel.some_function(args)()
 *        ↑ first ()  = pass arguments to the Python function
 *              ↑ second () = actually CALL it and get a Promise back
 *
 *   Without the second (), you just get a reference — not a result.
 *   This is the #1 Eel gotcha for beginners. Burn it into memory!
 */


// =============================================================================
// DOM Element References
// =============================================================================
// WHY grab these once at the top?
//   - Avoid repeated document.getElementById() calls (minor performance)
//   - Single place to update if HTML ids change (maintainability)
//   - Makes the event handler code below much cleaner (readability)

const btnNewProject    = document.getElementById("btn-new-project");
const projectInfoCard  = document.getElementById("project-info");
const noProjectMsg     = document.getElementById("no-project");
const displayName      = document.getElementById("display-project-name");
const displayModelDir  = document.getElementById("display-model-dir");
const displayCreatedAt = document.getElementById("display-created-at");


// =============================================================================
// Event Handlers
// =============================================================================

/**
 * Handle the full "New Project" workflow.
 *
 * WHY a standalone async function instead of an inline arrow function?
 *   1. Named functions show up in stack traces (easier debugging)
 *   2. Readable — you can see the whole workflow in one place
 *   3. Testable — you could call handleNewProject() from a test harness
 */
async function handleNewProject() {

    // --- Step 1: Open the folder picker ---
    // This call blocks (awaits) until the user picks a folder or cancels.
    console.log("Opening folder picker...");
    const browseResult = await eel.browse_for_model_directory()();

    // --- Step 2: Handle cancellation ---
    if (!browseResult.success) {
        console.log("User cancelled folder selection.");
        return;  // Do nothing — user changed their mind
    }

    console.log(`User selected: ${browseResult.path}`);

    // --- Step 3: Tell Python to create the ProjectIdentity ---
    const createResult = await eel.create_new_project(
        browseResult.path,
        browseResult.project_name
    )();

    // --- Step 4: Update the GUI ---
    if (createResult.success) {
        const project = createResult.project;

        // Populate the info card
        displayName.textContent      = project.project_name;
        displayModelDir.textContent  = project.model_directory;
        displayCreatedAt.textContent = formatTimestamp(project.created_at);

        // Show the card, hide the empty state
        projectInfoCard.classList.remove("hidden");
        noProjectMsg.classList.add("hidden");

        console.log("✅ Project created successfully.");

    } else {
        // Something went wrong on the Python side
        alert(`Error creating project: ${createResult.error}`);
        console.error("Project creation failed:", createResult.error);
    }
}


// =============================================================================
// Utility Functions
// =============================================================================

/**
 * Format an ISO timestamp into something human-friendly.
 *
 * WHY a utility function?
 *   - Timestamps will appear in many places as your app grows
 *   - One function to change if you want a different format later
 *   - Keeps the event handler clean and focused on LOGIC, not formatting
 *
 * @param {string} isoString — An ISO 8601 timestamp (e.g., "2025-10-15T14:30:00")
 * @returns {string} — Formatted like "Oct 15, 2025 — 2:30 PM"
 */
function formatTimestamp(isoString) {
    const date = new Date(isoString);
    return date.toLocaleDateString("en-US", {
        year: "numeric",
        month: "short",
        day: "numeric",
    }) + " — " + date.toLocaleTimeString("en-US", {
        hour: "numeric",
        minute: "2-digit",
    });
}


// =============================================================================
// Wire Up Events
// =============================================================================
// WHY addEventListener instead of onclick="..."?
//   - Separation of concerns: HTML structure vs. JS behavior
//   - You can attach multiple listeners to one element if needed
//   - Modern best practice — inline handlers are considered legacy

btnNewProject.addEventListener("click", handleNewProject);
