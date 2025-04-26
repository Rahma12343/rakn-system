// ✅ فتح وإغلاق نافذة الإشعارات
document.querySelector(".notification-icon").addEventListener("click", function () {
    const popup = document.getElementById("notificationPopup");
    popup.style.display = popup.style.display === "flex" ? "none" : "flex";

    if (popup.style.display === "flex") {
        loadNotifications();
    }
});

function closeNotificationPopup() {
    document.getElementById("notificationPopup").style.display = "none";
}

// ✅ تحميل إشعارات من الباك
async function loadNotifications() {
    const employeeId = localStorage.getItem("employee_id");
    const list = document.getElementById("notificationList");
    list.innerHTML = "";

    try {
        const response = await fetch(`http://127.0.0.1:8000/notification/${employeeId}?unread_only=false`);
        const data = await response.json();
        console.log("📩 Fetched notification data:", data);

        if (!data.notifications || !Array.isArray(data.notifications)) {
            updateNotifications(0);
            return;
        }

        const notifications = data.notifications;

        notifications.forEach(noti => {
            const item = document.createElement("li");

            const timestamp = noti.timestamp
                ? new Date(noti.timestamp).toLocaleString()
                : "No time";

            item.innerHTML = `
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: ${noti.message.includes('Warning') ? '#E0A800' : '#004AAB'};">
                        ${noti.message.includes('Warning') ? '⚠️' : '🚨'} ${noti.message}
                    </span>
                    <small style="color: gray; font-size: 11px;">${timestamp}</small>
                </div>
            `;
            
            list.appendChild(item);
        });

        updateNotifications(notifications.filter(n => !n.is_read).length);

        // ✅ تعليم كل الإشعارات كمقروءة بعد الفتح
        await markNotificationsAsRead(employeeId);

        // ✅ تصفير البادج فوق الجرس
        updateNotifications(0);

    } catch (error) {
        console.error("❌ Failed to load notifications:", error);
        updateNotifications(0);
    }
}


// ✅ تحديث رقم الإشعارات في الجرس
function updateNotifications(count) {
    const notificationBadge = document.querySelector(".notification-icon .badge");
    if (count > 0) {
        notificationBadge.textContent = count;
        notificationBadge.style.display = "flex";
    } else {
        notificationBadge.style.display = "none";
    }
}

// ✅ إشعار toast فوري
function showToastNotification(message) {
    let toast = document.createElement("div");
    toast.className = "toast-notification";
    toast.textContent = message.includes("Warning") ? `⚠️ ${message}` : `🚨 ${message}`;
    document.body.appendChild(toast);

    // ✅ تشغيل الصوت
    const audio = new Audio("../sounds/notif.mp3"); // عدّل المسار حسب مجلدك
    audio.play();

    setTimeout(() => {
        toast.classList.add("show");
    }, 100);

    setTimeout(() => {
        toast.classList.remove("show");
        document.body.removeChild(toast);
    }, 5000);
}

// ✅ التحقق من إشعارات جديدة كل 15 ثانية
let lastSeenNotificationId = null;

async function checkForNewNotifications() {
    const employeeId = localStorage.getItem("employee_id");
    if (!employeeId) return;

    try {
        const response = await fetch(`http://127.0.0.1:8000/notification/${employeeId}?unread_only=false`);
        const data = await response.json();

        if (!data.notifications || !Array.isArray(data.notifications)) {
            updateNotifications(0);
            return;
        }

        const notifications = data.notifications;

        if (notifications.length > 0) {
            const latest = notifications[0];

            if (lastSeenNotificationId === null) {
                // ✅ أول تحميل، نحدّث معرف آخر إشعار لكن ما نعرض شيء
                lastSeenNotificationId = latest.id;
            } else if (latest.id !== lastSeenNotificationId) {
                // ✅ في إشعار جديد، نعرض توست
                lastSeenNotificationId = latest.id;
                showToastNotification(latest.message);
                updateNotifications(notifications.filter(n => !n.is_read).length);
                
                // ✅ تحديث جدول المخالفات على الفور
                if (typeof fetchViolations === "function") {
                    fetchViolations();
                }
            }
        } else {
            updateNotifications(0);
        }
    } catch (err) {
        console.error("🚫 Error checking notifications:", err);
        updateNotifications(0);
    }
}

// ✅ عند تحميل الصفحة: أول تحميل وعد تناوبي
document.addEventListener("DOMContentLoaded", function () {
    const employeeId = localStorage.getItem("employee_id");
    if (employeeId) {
        loadNotifications();
        checkForNewNotifications();
        setInterval(checkForNewNotifications, 5000);
    }
});


async function markNotificationsAsRead(employeeId) {
    try {
        await fetch(`http://127.0.0.1:8000/notification/mark_read/${employeeId}`, {
            method: "POST",
        });
        console.log("🔵 Notifications marked as read");
    } catch (error) {
        console.error("❌ Failed to mark notifications as read:", error);
    }
}
