document.getElementById("newProjectBtn").addEventListener("click", async () => {
  // Call Python to open native folder picker
  const folder = await eel.choose_model_directory()();

  const pathBox = document.getElementById("pathBox");

  if (!folder) {
    pathBox.textContent = "(canceled)";
    return;
  }

  pathBox.textContent = folder;
});
