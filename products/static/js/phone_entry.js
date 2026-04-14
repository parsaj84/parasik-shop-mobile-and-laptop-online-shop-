document.addEventListener("DOMContentLoaded", function () {
  const inputField = document.querySelector("input[type='text']");
  const errorMessage = document.querySelector("p.text-error");
  const submitButton = document.querySelector(".submit-btn");
  const form = document.querySelector("form")
  

  form.addEventListener("submit", function(e) {
    let entry = inputField.value
    let error = validateInput(entry)
    if (!error) {
      submitButton.classList.add("submit-btn-invisable")
    } else {
      e.preventDefault()
    }
  });

  function validateInput(value) {
    
    const phonePattern = /^09\d{9}$/;

    if (!value) {
      return "این فیلد نمی‌تواند خالی باشد";
    } else if (!phonePattern.test(value)) {
      return "لطفا شماره موبایل معتبر وارد کنید";
    }
    return "";
  }

  inputField?.addEventListener("input", function () {
    const error = validateInput(inputField.value.trim());

    if (error) {
      errorMessage.textContent = error;
      errorMessage.classList.add("active");
      submitButton.classList.add("submit-btn-invisable");
    } else {
      errorMessage.textContent = "";
      errorMessage.classList.remove("active");
      submitButton.classList.remove("submit-btn-invisable");
    }
  });
});



const DARK_THEME = 'dark';
const LIGHT_THEME = 'light';

const themeToggleButtons = document.querySelectorAll('.toggle-theme');

const toggleTheme = () => {
  const isDarkMode = localStorage.getItem('theme') === DARK_THEME;
  document.documentElement.classList.toggle(DARK_THEME, !isDarkMode);
  localStorage.setItem('theme', isDarkMode ? LIGHT_THEME : DARK_THEME);
};


// Event Listeners for Theme Toggle
// Add click listeners to toggle theme buttons
themeToggleButtons.forEach(button => {
  button.addEventListener('click', toggleTheme);
});


