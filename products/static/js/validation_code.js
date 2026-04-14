
document.addEventListener('DOMContentLoaded', () => {
  const form = document.getElementById('otp-form')
  const secoundForm = document.getElementById("otp-form-1")


  if (!form) return

  const inputs = secoundForm ? [...form.querySelectorAll('input[type=text]'), ...secoundForm.querySelectorAll("input[type=text")] : [...form.querySelectorAll('input[type=text]')]
  const submit = form.querySelector('button[type=submit]')

  const handleKeyDown = (e) => {
    if (
      !/^[0-9]{1}$/.test(e.key)
      && e.key !== 'Backspace'
      && e.key !== 'Delete'
      && e.key !== 'Tab'
      && !e.metaKey
    ) {
      e.preventDefault()
    }

    if (e.key === 'Delete' || e.key === 'Backspace') {
      const index = inputs.indexOf(e.target);
      if (index > 0) {
         submit.classList.add("submit-btn-invisable")
        inputs[index - 1].value = '';
        inputs[index - 1].focus();
      }
    }
  }

  const handleInput = (e) => {
    const { target } = e
    const index = inputs.indexOf(target)
    if (target.value) {
      if (index < inputs.length - 1) {
        inputs[index + 1].focus()
      } else {
        submit.classList.remove("submit-btn-invisable")
        submit.focus()
      }
    }
  }

  form.addEventListener("submit", function(e) {
    e.target.classList.add("submit-btn-invisable")
  })

  const handleFocus = (e) => {
    e.target.select()
  }

  const handlePaste = (e) => {
    e.preventDefault()
    const text = e.clipboardData.getData('text')
    if (!new RegExp(`^[0-9]{${inputs.length}}$`).test(text)) {
      return
    }
    const digits = text.split('')
    inputs.forEach((input, index) => input.value = digits[index])
    submit.focus()
  }

  inputs.forEach((input) => {
    input.addEventListener('input', handleInput)
    input.addEventListener('keydown', handleKeyDown)
    input.addEventListener('focus', handleFocus)
    input.addEventListener('paste', handlePaste)
  })
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






// ajax requests

$(document).ready(function () {
  let dataTag = $(".validation-code-data")
  let urlResendvalidationCode = dataTag.data("url-resend-validation-code")

    let loadingSection = $("#loadingSection")
    let loadingModal = $("#loaingModal")
    $(document).ajaxStart(function (e) {
        loadingSection.css("display", "flex")
        loadingModal.addClass("active")
    });
    $(document).ajaxStop(function (E) {
        loadingSection.css("display", "none")
        loadingModal.removeClass("active")
    });


  let interval = null
  function setTimer() {
    let timer = document.querySelector(".login-timer");
    if (timer) {
      let time = parseInt(timer.dataset.time, 10);

      interval = setInterval(() => {
        if (time > 0) {
          time -= 1;
          let minutes = Math.floor(time / 60);
          let seconds = Math.floor(time % 60);
          let text = `${minutes}:${seconds.toString().padStart(2, "0")}`;
          timer.innerHTML = text;
        } else {
          clearInterval(interval);
          let timerText = document.querySelector(".login-timer_text");
          if (timerText) timerText.style.display = "none";
          let resendBtn = document.querySelector(".resend-code");
          if (resendBtn) resendBtn.classList.add("active");
        }
      }, 1000);
    }
  }
  clearInterval(interval)
  setTimer()
  let timerElement = $(".login-timer")
  $(".resend-code").on("click", function (e) {
    let btn = $(this)
    $.ajax({
      url: urlResendvalidationCode,
      method: "GET",
      data: { "sent_from_login": "true" },
      success: function (data) {
        if (data.success) {
          $(".login-timer_text").css("display", "flex")
          timerElement.attr("data-time", 180)
          btn.removeClass("active")
          clearInterval(interval)
          setTimer()
        } else {
          fireAlert(text = "خطایی رخ داد!", icon = "error", title = "خطا!")
        }
      }
    });
  });
});