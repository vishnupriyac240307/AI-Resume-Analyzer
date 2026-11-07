const fileInput = document.getElementById("resumeFile");
const fileSelected = document.getElementById("fileSelected");
const dropZone = document.getElementById("dropZone");

function showFile(file) {
  if (!fileSelected || !file) return;
  const size = (file.size / (1024 * 1024)).toFixed(2);
  fileSelected.textContent = `Selected: ${file.name} (${size} MB)`;
  fileSelected.classList.add("visible");
}
if (fileInput) {
  fileInput.addEventListener("change", () => showFile(fileInput.files[0]));
}
if (dropZone && fileInput) {
  ["dragenter", "dragover"].forEach(eventName => dropZone.addEventListener(eventName, e => {
    e.preventDefault(); dropZone.classList.add("dragging");
  }));
  ["dragleave", "drop"].forEach(eventName => dropZone.addEventListener(eventName, e => {
    e.preventDefault(); dropZone.classList.remove("dragging");
  }));
  dropZone.addEventListener("drop", e => {
    if (e.dataTransfer.files.length) {
      fileInput.files = e.dataTransfer.files;
      showFile(e.dataTransfer.files[0]);
    }
  });
}
