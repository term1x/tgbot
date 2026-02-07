/* global Telegram, QRious */

const API_BASE = window.location.origin;
let accessToken = "";
let devices = [];

const views = document.querySelectorAll(".view");
const navButtons = document.querySelectorAll("nav button");
const usernameEl = document.getElementById("username");
const balanceEl = document.getElementById("balance");
const deviceCountEl = document.getElementById("device-count");
const deviceListEl = document.getElementById("device-list");
const vlessLinkEl = document.getElementById("vless-link");
const qrCanvas = document.getElementById("qr");
const topupButton = document.getElementById("topup-button");
const addDeviceButton = document.getElementById("add-device");
const disableDeviceButton = document.getElementById("disable-device");

const qr = new QRious({ element: qrCanvas, size: 200, value: "" });

function showView(viewId) {
  views.forEach((view) => view.classList.remove("active"));
  document.getElementById(viewId).classList.add("active");
}

navButtons.forEach((button) => {
  button.addEventListener("click", () => {
    showView(button.dataset.view);
  });
});

async function apiFetch(path, options = {}) {
  const headers = options.headers || {};
  if (accessToken) {
    headers.Authorization = `Bearer ${accessToken}`;
  }
  const response = await fetch(`${API_BASE}${path}`, { ...options, headers });
  if (!response.ok) {
    throw new Error("API error");
  }
  return response.json();
}

async function authenticate() {
  const initData = Telegram.WebApp.initData;
  const body = new URLSearchParams();
  body.set("init_data", initData);

  const response = await fetch(`${API_BASE}/auth`, {
    method: "POST",
    body,
  });
  const data = await response.json();
  accessToken = data.access_token;
}

async function loadDashboard() {
  const user = await apiFetch("/me");
  usernameEl.textContent = user.username || "@unknown";
  balanceEl.textContent = user.balance;

  devices = await apiFetch("/devices");
  deviceCountEl.textContent = devices.length;
  renderDevices();
}

function renderDevices() {
  deviceListEl.innerHTML = "";
  devices.forEach((device) => {
    const item = document.createElement("li");
    item.textContent = `${device.uuid} ${device.active ? "(active)" : "(disabled)"}`;
    item.addEventListener("click", () => showDeviceDetails(device));
    deviceListEl.appendChild(item);
  });
}

function showDeviceDetails(device) {
  vlessLinkEl.textContent = device.vless_link;
  qr.set({ value: device.vless_link });
  showView("device-details");
}

addDeviceButton.addEventListener("click", async () => {
  const device = await apiFetch("/devices", { method: "POST" });
  devices.push(device);
  renderDevices();
  showDeviceDetails(device);
});

disableDeviceButton.addEventListener("click", async () => {
  const activeDevice = devices.find((device) => device.active);
  if (!activeDevice) {
    return;
  }
  await apiFetch(`/devices/${activeDevice.id}`, { method: "DELETE" });
  activeDevice.active = false;
  renderDevices();
});

topupButton.addEventListener("click", async () => {
  const amount = document.getElementById("topup-amount").value;
  if (!amount) {
    return;
  }
  await apiFetch("/balance/topup", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ amount }),
  });
  await loadDashboard();
});

window.addEventListener("load", async () => {
  try {
    Telegram.WebApp.ready();
    await authenticate();
    await loadDashboard();
  } catch (error) {
    console.error(error);
  }
});
