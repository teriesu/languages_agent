document.addEventListener("DOMContentLoaded", () => {
  const select = document.getElementById("lesson-select");
  const lessonDescription = document.getElementById("lesson-description");
  const hiddenInput = document.getElementById("selected-lesson");

  const syncLesson = () => {
    if (!select) return;
    const option = select.selectedOptions[0];
    if (!option) return;
    if (hiddenInput) {
      hiddenInput.value = option.value;
    }
    if (lessonDescription) {
      lessonDescription.textContent = option.dataset.description || "No description yet.";
    }
  };

  if (select) {
    select.addEventListener("change", () => {
      syncLesson();
      const form = document.getElementById("message-form");
      form?.scrollIntoView({ behavior: "smooth" });
    });
  }

  syncLesson();
});
