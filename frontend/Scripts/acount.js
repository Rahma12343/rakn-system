document.addEventListener("DOMContentLoaded", function () {
    const userData = localStorage.getItem("securityUser");

    if (!userData) {
        alert("You are not logged in. Please login first.");
        window.location.href = "login.html";
        return;
    }

    const user = JSON.parse(userData);

    // ✅ تعبئة الحقول من بيانات المستخدم
    document.getElementById("name").value = user.name || "";
    document.getElementById("id").value = user.employee_id || "";
    document.getElementById("phone").value = user.phone || "";

    // ✅ عرض صورة الوجه في الحساب
    if (user.face_image) {
        document.getElementById("profilePic").src = user.face_image;
    }

    // ✅ عرض صورة الوجه والهيدر معاً (اختياري)
    if (user.face_image && document.getElementById("profile-image")) {
        document.getElementById("profile-image").src = user.face_image;
    }

    // ✅ تجهيز زر تسجيل الخروج بدون تكرار DOMContentLoaded
    const logoutBtn = document.getElementById("logoutBtn");

    if (logoutBtn) {
        logoutBtn.addEventListener("click", function (e) {
            e.preventDefault(); // منع الانتقال العادي

            // ✅ حذف بيانات تسجيل الدخول
            localStorage.removeItem("securityUser");

            // ✅ إعادة التوجيه إلى الصفحة الرئيسية
            window.location.href = "/";
        });
    }
});
