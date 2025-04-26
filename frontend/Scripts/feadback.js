// الحصول على العناصر
const modal = document.getElementById("feedbackModal");
const openLink = document.getElementById("openFeedbackLink");
const closeBtn = document.querySelector(".close");

// عند الضغط على رابط "Feedback"
openLink.onclick = function (event) {
    event.preventDefault(); // منع التنقل إلى صفحة جديدة
    modal.style.display = "flex";
};

// عند الضغط على زر الإغلاق
closeBtn.onclick = function () {
    modal.style.display = "none";
};

// إغلاق النافذة عند الضغط خارجها
window.onclick = function (event) {
    if (event.target === modal) {
        modal.style.display = "none";
    }
};
