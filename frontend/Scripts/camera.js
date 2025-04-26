//-------------------------------------------------------------
//صفحه الكاميرا 

// تفعيل عرض/إخفاء الجداول وتفعيل الأزرار
document.addEventListener("DOMContentLoaded", function () {
  const cameraButtons = document.querySelectorAll(".camera-btn");
  const cameraLists = document.querySelectorAll(".camera-list");

  cameraButtons.forEach((button, index) => {
    button.addEventListener("click", () => {
      cameraLists.forEach((list) => (list.style.display = "none"));
      cameraLists[index].style.display = "block";
    });
  });

  cameraButtons.forEach((button) => {
    button.addEventListener("click", function () {
      cameraButtons.forEach((btn) => btn.classList.remove("active"));
      this.classList.add("active");
    });
  });
});

// فتح وإغلاق مودالات الإضافة
function openAddDroneModal() {
  document.getElementById("addDroneModal").style.display = "flex";
}

function closeAddDroneModal() {
  document.getElementById("addDroneModal").style.display = "none";
}

function openAddGateModal() {
  document.getElementById("addGateModal").style.display = "flex";
}

function closeAddGateModal() {
  document.getElementById("addGateModal").style.display = "none";
}

// ✅ إضافة درون
const droneForm = document.getElementById("droneForm");
droneForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const model = this.model.value;
  const battery = this.battery.value;
  const brand = this.brand.value;
  const color = this.color.value;
  const status = this.status.value;

  const droneData = { model, battery, brand, color, status };

  fetch("http://127.0.0.1:8000/camera/add-drone", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(droneData),
  })
    .then((res) => res.json())
    .then((data) => {
      const row = document.createElement("tr");
      row.setAttribute("data-id", data.camera_id);
      row.innerHTML = `
        <td class="auto-number"></td>
        <td>${model}</td>
        <td>${battery}</td>
        <td>${brand}</td>
        <td>${color}</td>
        <td>${status}</td>
        <td>
          <div class="action-buttons">
            <button class="delete-btn" onclick="deleteRow(this)">🗑️</button>
            <button class="edit-btn" onclick="openEditDroneModal(this)">✏️</button>
          </div>
        </td>
      `;
      document.getElementById("droneBody").appendChild(row);
      alert("✅ Drone added successfully");
      droneForm.reset();
      closeAddDroneModal();
    });
});


// ✅ إضافة كاميرا بوابة وربطها بالباكند
const gateCameraForm = document.getElementById("gateCameraForm");
gateCameraForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const model = this.model.value;
  const resolution = this.resolution.value;
  const brand = this.brand.value;
  const color = this.color.value;
  const status = this.status.value;

  const cameraData = { model, resolution, brand, color, status };

  fetch("http://127.0.0.1:8000/camera/add-gate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(cameraData),
  })
    .then((res) => res.json())
    .then((data) => {
      const row = document.createElement("tr");
      row.setAttribute("data-id", data.camera_id);
      row.innerHTML = `
        <td class="auto-number"></td>
        <td>${model}</td>
        <td>${resolution}</td>
        <td>${brand}</td>
        <td>${color}</td>
        <td>${status}</td>
        <td>
          <div class="action-buttons">
            <button class="delete-btn" onclick="deleteRow(this)">🗑️</button>
            <button class="edit-btn" onclick="openEditGateCameraModal(this)">✏️</button>
          </div>
        </td>
      `;
      document.getElementById("gateCameraBody").appendChild(row);
      alert("✅ Gate camera added successfully");
      gateCameraForm.reset();
      closeAddGateModal();
    })
    .catch((err) => {
      console.error(err);
      alert("❌ Error adding gate camera");
    });
});

//------------------------------------------------------------------------------



// ✅ تعديل درون وربطه بالباكند
function openEditDroneModal(button) {
  const row = button.closest("tr");
  const cells = row.querySelectorAll("td");

  document.getElementById("editDroneModel").value = cells[1].textContent;
  document.getElementById("editDroneBattery").value = cells[2].textContent;
  document.getElementById("editDroneBrand").value = cells[3].textContent;
  document.getElementById("editDroneColor").value = cells[4].textContent;
  document.getElementById("editDroneStatus").value = cells[5].textContent;

  window.currentDroneRow = row;
  document.getElementById("editDroneModal").style.display = "flex";
}

function closeEditDroneModal() {
  document.getElementById("editDroneModal").style.display = "none";
}

document.getElementById("editDroneForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const row = window.currentDroneRow;
  const cameraId = row.getAttribute("data-id");

  const model = document.getElementById("editDroneModel").value;
  const battery = document.getElementById("editDroneBattery").value;
  const brand = document.getElementById("editDroneBrand").value;
  const color = document.getElementById("editDroneColor").value;
  const status = document.getElementById("editDroneStatus").value;

  fetch(`http://127.0.0.1:8000/camera/drone/${cameraId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model, battery, brand, color, status }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to update drone");

      row.cells[1].textContent = model;
      row.cells[2].textContent = battery;
      row.cells[3].textContent = brand;
      row.cells[4].textContent = color;
      row.cells[5].textContent = status;
      closeEditDroneModal();
      alert("✅ Drone updated");
    })
    .catch((err) => {
      console.error(err);
      alert("❌ Error updating drone");
    });
});

// ✅ تعديل كاميرا بوابة وربطها بالباكند
function openEditGateCameraModal(button) {
  const row = button.closest("tr");
  const cells = row.querySelectorAll("td");

  document.getElementById("editModel").value = cells[1].textContent;
  document.getElementById("editResolution").value = cells[2].textContent;
  document.getElementById("editBrand").value = cells[3].textContent;
  document.getElementById("editColor").value = cells[4].textContent;
  document.getElementById("editStatus").value = cells[5].textContent;

  window.currentGateCameraRow = row;
  document.getElementById("editGateCameraModal").style.display = "flex";
}

function closeEditGateCameraModal() {
  document.getElementById("editGateCameraModal").style.display = "none";
}

document.getElementById("editGateCameraForm").addEventListener("submit", function (e) {
  e.preventDefault();
  const row = window.currentGateCameraRow;
  const cameraId = row.getAttribute("data-id");

  const model = document.getElementById("editModel").value;
  const resolution = document.getElementById("editResolution").value;
  const brand = document.getElementById("editBrand").value;
  const color = document.getElementById("editColor").value;
  const status = document.getElementById("editStatus").value;

  fetch(`http://127.0.0.1:8000/camera/gate/${cameraId}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ model, resolution, brand, color, status }),
  })
    .then((res) => {
      if (!res.ok) throw new Error("Failed to update gate camera");

      row.cells[1].textContent = model;
      row.cells[2].textContent = resolution;
      row.cells[3].textContent = brand;
      row.cells[4].textContent = color;
      row.cells[5].textContent = status;
      closeEditGateCameraModal();
      alert("✅ Gate camera updated");
    })
    .catch((err) => {
      console.error(err);
      alert("❌ Error updating gate camera");
    });
});

//----------------------------------------------------
//حذف الكاميرا
//درون
function deleteDroneFromBackend(cameraId, row) {
  fetch(`http://127.0.0.1:8000/camera/drone/${cameraId}`, {
    method: "DELETE",
  })
    .then((res) => {
      if (!res.ok) throw new Error("❌ Failed to delete drone");
      row.remove();
      alert("✅ Drone deleted");
    })
    .catch((err) => {
      console.error(err);
      alert("❌ Error deleting drone");
    });
}

//بوابه 
function deleteGateCameraFromBackend(cameraId, row) {
  fetch(`http://127.0.0.1:8000/camera/gate/${cameraId}`, {
    method: "DELETE",
  })
    .then((res) => {
      if (!res.ok) throw new Error("❌ Failed to delete gate camera");
      row.remove();
      alert("✅ Gate camera deleted");
    })
    .catch((err) => {
      console.error(err);
      alert("❌ Error deleting gate camera");
    });
}

//حذف موحد
function deleteRow(btn) {
  const row = btn.closest("tr");
  const tableType = row.closest("tbody").id;
  const cameraId = row.getAttribute("data-id");

  if (!cameraId) {
    alert("❌ Camera ID not found");
    return;
  }

  if (confirm("Are you sure you want to delete this camera?")) {
    if (tableType === "droneBody") {
      deleteDroneFromBackend(cameraId, row);
    } else if (tableType === "gateCameraBody") {
      deleteGateCameraFromBackend(cameraId, row);
    }
  }
}



//-------------------------------------------------------
function loadDronesFromBackend() {
  fetch("http://127.0.0.1:8000/camera/drones")
    .then(res => res.json())
    .then(drones => {
      const droneBody = document.getElementById("droneBody");
      droneBody.innerHTML = ""; // تفريغ الجدول قبل التعبئة

      drones.forEach(drone => {
        const row = document.createElement("tr");
        row.setAttribute("data-id", drone.camera_id);
        row.innerHTML = `
          <td class="auto-number"></td>
          <td>${drone.model}</td>
          <td>${drone.battery}</td>
          <td>${drone.brand}</td>
          <td>${drone.color}</td>
          <td>${drone.status}</td>
          <td>
            <div class="action-buttons">
              <button class="delete-btn" onclick="deleteRow(this)">🗑️</button>
              <button class="edit-btn" onclick="openEditDroneModal(this)">✏️</button>
            </div>
          </td>
        `;
        droneBody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Error loading drones:", err);
    });
}


function loadGateCamerasFromBackend() {
  fetch("http://127.0.0.1:8000/camera/gates")
    .then(res => res.json())
    .then(cameras => {
      const gateBody = document.getElementById("gateCameraBody");
      gateBody.innerHTML = ""; // تفريغ الجدول قبل التعبئة

      cameras.forEach(cam => {
        const row = document.createElement("tr");
        row.setAttribute("data-id", cam.camera_id);
        row.innerHTML = `
          <td class="auto-number"></td>
          <td>${cam.model}</td>
          <td>${cam.resolution}</td>
          <td>${cam.brand}</td>
          <td>${cam.color}</td>
          <td>${cam.status}</td>
          <td>
            <div class="action-buttons">
              <button class="delete-btn" onclick="deleteRow(this)">🗑️</button>
              <button class="edit-btn" onclick="openEditGateCameraModal(this)">✏️</button>
            </div>
          </td>
        `;
        gateBody.appendChild(row);
      });
    })
    .catch(err => {
      console.error("Error loading gate cameras:", err);
    });
}

loadDronesFromBackend();
loadGateCamerasFromBackend();


//***************************** */
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
