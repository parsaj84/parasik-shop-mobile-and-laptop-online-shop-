document.addEventListener("DOMContentLoaded", function () {
  const passwordInput = document.getElementById("passwordInput");
  const passwordLoginInput = document.getElementById("passwordLoginInput")
  const confirmPassword = document.getElementById("confirmPassword");
  const passwordLoginBtn = document.getElementById("passwordLoginBtn")
  const error = document.querySelector(".text-error.active")
  const passwordLoginForm = document.getElementById("passwordLoginForm")
  const bar1 = document.getElementById("bar1");
  const bar2 = document.getElementById("bar2");
  const bar3 = document.getElementById("bar3");

  const lengthCheck = document.getElementById("lengthCheck");
  const numberCheck = document.getElementById("numberCheck");
  const uppercaseCheck = document.getElementById("uppercaseCheck");

  let passwordEditBtn = document.getElementById("passwordEditBtn")

  passwordLoginForm?.addEventListener("submit", function(e) {
    let entry = passwordLoginInput.value
    if (!entry) {
      e.preventDefault()
      error.innerText = "لطفا رمز عبور را وارد کنید!"

    } else {
      passwordLoginBtn?.classList.add("submit-btn-invisable")
    } 
  });

  passwordInput?.addEventListener("input", function () {
    let password = passwordInput.value;
    let isLengthValid = password.length >= 8;
    let hasNumber = /[0-9]/.test(password);
    let hasUppercase = /[A-Z]/.test(password);
    

    updateRequirement(lengthCheck, isLengthValid);
    updateRequirement(numberCheck, hasNumber);
    updateRequirement(uppercaseCheck, hasUppercase);

    let strength = isLengthValid + hasNumber + hasUppercase;

    resetBars();

    if (strength === 1) {
      bar1.classList.replace("bg-gray-300", "bg-red-500");
      passwordEditBtn.classList.add("submit-btn-invisable")
    } else if (strength === 2) {
      bar1.classList.replace("bg-gray-300", "bg-amber-400");
      bar2.classList.replace("bg-gray-300", "bg-amber-400");
      passwordEditBtn.classList.add("submit-btn-invisable")
    } else if (strength === 3) {
      bar1.classList.replace("bg-gray-300", "bg-green-500");
      bar2.classList.replace("bg-gray-300", "bg-green-500");
      bar3.classList.replace("bg-gray-300", "bg-green-500");
      passwordEditBtn.classList.remove("submit-btn-invisable")
    }
  });

  function updateRequirement(element, isValid) {
    element.style.display = isValid ? "none" : "flex";
  }

  function resetBars() {
    [bar1, bar2, bar3].forEach(bar => {
      bar.classList.remove("bg-red-500", "bg-amber-400", "bg-green-500");
      bar.classList.add("bg-gray-300");
    });
  }

  document.querySelectorAll(".toggle-password").forEach(button => {
    button.addEventListener("click", function () {
      const input = this.parentElement.querySelector("input");
      const inputType = input.getAttribute("type")
      if (input.type === "password") {
        input.type = "text";
        this.querySelector("svg use").setAttribute("href", "#eye-slash")
      } else {
        input.type = "password";
        this.querySelector("svg use").setAttribute("href", "#eye")
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

document.getElementById("passwordSetForm").addEventListener("submit", function(e) {
  const password = e.target.querySelector("[name=password]").value
  const passwordConfirm = e.target.querySelector("[name=password-confirm]").value
  const error = e.target.querySelector(".text-error")
  if (password !== passwordConfirm) {
    error.innerText = "تایید رمز عبور باید با رمز عبور یکی باشد!"
    e.preventDefault()
  } else {
    passwordEditBtn.classList.add("submit-btn-invisable")
  }
});

  // confirmPassword?.addEventListener("input", function () {
  //   if (confirmPassword.value !== passwordInput.value) {
  //     confirmPassword.setCustomValidity("رمز عبور تطابق ندارد");
  //   } else {
  //     confirmPassword.setCustomValidity("");
  //   }
  // });
});

