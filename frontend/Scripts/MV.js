// ✅ جلب المخالفات عند فتح الصفحة + فلترة حسب التاريخ + نافذة التفاصيل

let violationData = [];

// ✅ جلب المخالفات من الباك
async function fetchViolations(from = "", to = "") {
    let url = "http://127.0.0.1:8000/violation/violations";
    if (from && to) {
        url += `?from_date=${from}&to_date=${to}`;
    }

    try {
        const response = await fetch(url);
        const data = await response.json();
        console.log("✅ Fetched data:", data);
        violationData = data;
        loadTableData(violationData);
    } catch (error) {
        console.error("❌ Error fetching violations:", error);
    }
}

// ✅ فلترة حسب التاريخ
function filterTable() {
    const fromDate = document.getElementById("fromDate").value;
    const toDate = document.getElementById("toDate").value;
    fetchViolations(fromDate, toDate);
}

// ✅ تحميل الصفحة: جلب مخالفات + تفعيل أيقونة التاريخ
document.addEventListener("DOMContentLoaded", function () {
    fetchViolations();

    let dateContainers = document.querySelectorAll(".date-input-container");
    dateContainers.forEach(container => {
        let icon = container.querySelector(".calendar-icon");
        let input = container.querySelector("input[type='date']");

        icon.addEventListener("click", function () {
            input.showPicker();
            icon.classList.add("clicked-effect");
            setTimeout(() => {
                icon.classList.remove("clicked-effect");
            }, 200);
        });
    });
});

// ✅ عرض تفاصيل المخالفة في نافذة منبثقة
const modal = document.getElementById("violationModal");
const closeModal = document.querySelector(".close-btn");

window.showDetails = async function (id) {
    try {
        const response = await fetch(`http://127.0.0.1:8000/violation/violations/${id}`);
        const violation = await response.json();
        console.log("🧐 Violation details:", violation);

        document.getElementById("violationNumber").textContent = violation.violation_id;
        document.getElementById("violationName").textContent = violation.employee_name;
        document.getElementById("violationID").textContent = violation.employee_id;
        document.getElementById("licensePlate").textContent = violation.license_plate;
        document.getElementById("violationDate").textContent = violation.date;
        document.getElementById("violationTime").textContent = violation.time;

        const imageElement = document.getElementById("violationImage");
        if (violation.image_url) {
            imageElement.src = violation.image_url;
            imageElement.style.display = "block";
        } else {
            imageElement.style.display = "none";
        }

        modal.style.display = "flex";
    } catch (error) {
        console.error("❌ Failed to fetch violation details:", error);
    }
};

// ✅ إغلاق النافذة
closeModal.onclick = () => modal.style.display = "none";
window.onclick = (e) => {
    if (e.target === modal) modal.style.display = "none";
};

// ✅ دالة عرض البيانات داخل الجدول
function loadTableData(data) {
    console.log("📊 Loading table with data:", data);

    const tableBody = document.querySelector("#violationTable tbody");
    tableBody.innerHTML = "";

    data.forEach((violation) => {
        const row = document.createElement("tr");

        row.innerHTML = `
        <td>${violation.violation_id}</td>
        <td style="color: ${violation.violation_type === 'Warning' ? 'orange' : 'red'};">
            ${violation.violation_type}
        </td>
        <td>${violation.date}</td>
        <td>${violation.time}</td>
        <td>
            <img src="../images/detailsGray.svg" class="details-icon" onclick="showDetails('${violation.violation_id}')">
        </td>
    `;
    
        tableBody.appendChild(row);
    });
}
//------------------------------------------------------------
    
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




/*---------------------------------------*/
