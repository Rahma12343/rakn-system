

/* حق التوب بار */
/*----------------------------------*/

/* حق عرض الاسم والاي دي */ 
document.addEventListener("DOMContentLoaded", () => {
    const user = JSON.parse(localStorage.getItem("securityUser"));

    if (user) {
        // تحديث الاسم
        const nameEl = document.getElementById("user-name");
        if (nameEl) nameEl.textContent = user.name || "Unknown";

        // تحديث ID
        const idEl = document.getElementById("user-id");
        if (idEl) idEl.textContent = user.employee_id || "No ID";

        // تحديث الصورة
        const imageEl = document.getElementById("profile-image");
        if (imageEl && user.face_image && user.face_image !== "") {
            imageEl.src = user.face_image;
        }
    } else {
        // إعادة التوجيه لصفحة تسجيل الدخول إذا ما في بيانات
        window.location.href = "login.html";
    }
});


//حق التاريخ الي في التوب بار
document.addEventListener("DOMContentLoaded", function () {
    function updateDate() {
        let today = new Date();
        let options = { year: "numeric", month: "long", day: "numeric" };
        let formattedDate = today.toLocaleDateString("en-US", options);

        document.getElementById("current-date").textContent = formattedDate;
    }

    updateDate();
});




document.getElementById("toggleSidebar").addEventListener("click", toggleSidebar);
document.getElementById("toggleSidebarTop").addEventListener("click", toggleSidebar);

function toggleSidebar() {
    let sidebar = document.getElementById("sidebar");
    let content = document.querySelector(".content");
    let topbar = document.querySelector(".topbar");
    let toggleSidebarTop = document.getElementById("toggleSidebarTop");

    sidebar.classList.toggle("collapsed");
    content.classList.toggle("expanded");
    topbar.classList.toggle("expanded");

    // إظهار زر التوب بار فقط عند إخفاء الشريط الجانبي
    if (sidebar.classList.contains("collapsed")) {
        toggleSidebarTop.style.display = "flex";
    } else {
        toggleSidebarTop.style.display = "none";
    }
}

document.addEventListener("DOMContentLoaded", function () {
    let currentLocation = window.location.pathname.split("/").pop(); // استخراج اسم الصفحة الحالي
    let menuLinks = document.querySelectorAll(".menu-link");

    menuLinks.forEach(link => {
        if (link.getAttribute("href") === currentLocation) {
            link.classList.add("active");
        }
    });
});





//-------------------------------------------------------------------

    
document.addEventListener("DOMContentLoaded", function () {
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault(); // منع الانتقال العادي

            // ✅ حذف بيانات تسجيل الدخول
            localStorage.removeItem("securityUser");

            // ✅ إعادة التوجيه إلى الصفحة الرئيسية (index.html)
            window.location.href = "/";
        });
    }
});








function togglePassword() {
    const passwordInput = document.getElementById("password");
    const eyeIcon = document.getElementById("eyeIcon");
    const eyeText = document.getElementById("eyeText");

    if (passwordInput.type === "password") {
        passwordInput.type = "text";
        eyeText.textContent = "Show";
        eyeIcon.src = "../images/315219_hidden_eye_icon.svg"; // ضع هنا أيقونة "عين مفتوحة"
    } else {
        passwordInput.type = "password";
        eyeText.textContent = "Hide";
        eyeIcon.src = "../images/315220_eye_icon.svg"; // أيقونة "عين مغلقة"
    }
}


/*------------------------*/
