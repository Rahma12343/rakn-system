document.addEventListener("DOMContentLoaded", function () {
    const idInput = document.querySelector("input[name='id']");
    const passwordInput = document.getElementById("passwordField");
    const signInButton = document.getElementById("signInButton");
    const eyeIcon = document.getElementById("eyeIcon");
    const eyeText = document.getElementById("eyeText");
    const toggleVisibility = document.querySelector(".toggle_visibility");
    const form = document.querySelector(".form_fields");

    if (!idInput || !passwordInput || !signInButton || !eyeIcon || !eyeText || !form) {
        console.error("Error: Some elements are missing in the DOM.");
        return;
    }

    function togglePassword() {
        if (passwordInput.type === "password") {
            passwordInput.type = "text";
            eyeIcon.src = "../images/315220_eye_icon.svg";
            eyeText.innerText = "Hide";
        } else {
            passwordInput.type = "password";
            eyeIcon.src = "../images/315219_hidden_eye_icon.svg";
            eyeText.innerText = "Show";
        }
    }

    function checkFormCompletion() {
        const isIdValid = idInput.value.trim().length > 0;
        const isPasswordValid = passwordInput.value.trim().length > 0;

        if (isIdValid && isPasswordValid) {
            signInButton.disabled = false;
            signInButton.classList.add("enabled");
        } else {
            signInButton.disabled = true;
            signInButton.classList.remove("enabled");
        }
    }

    idInput.addEventListener("input", checkFormCompletion);
    passwordInput.addEventListener("input", checkFormCompletion);
    checkFormCompletion();

    if (toggleVisibility) {
        toggleVisibility.addEventListener("click", togglePassword);
    }

    form.addEventListener("submit", async function (event) {
        event.preventDefault();

        const securityId = idInput.value.trim();
        const password = passwordInput.value.trim();

        if (!securityId || !password) {
            alert("Please fill in both ID and password.");
            return;
        }

        try {
            const response = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    employee_id: securityId,
                    password: password
                })
            });

            if (response.ok) {
                const data = await response.json();
                console.log("Login successful:", data);

                // ✅ تحقق إذا كان الموظف من الأمن (role = 0)
                if (data.user.role === 0) {
                    localStorage.setItem("securityUser", JSON.stringify(data.user));
                    localStorage.setItem("employee_id", data.user.employee_id); // ✅ هنا نضيفه

                    window.location.href = "HomePage.html";
                }
                 else {
                    alert("You are not authorized to access this system. Security staff only.");
                }
            } else {
                const errorData = await response.json();
                alert("Login failed: " + errorData.detail);
            }
        } catch (error) {
            console.error("Error during login:", error);
            alert("Network error or server is down.");
        }
    });
});
