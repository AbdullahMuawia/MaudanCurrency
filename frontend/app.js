const API_BASE = "https://currencywise-backend.onrender.com/api";

const amountInput   = document.getElementById("amount");
const fromSelect    = document.getElementById("from-currency");
const toSelect      = document.getElementById("to-currency");
const convertBtn    = document.getElementById("convert-btn");
const swapBtn       = document.getElementById("swap-btn");
const resultDiv     = document.getElementById("result");
const resultText    = document.getElementById("result-text");
const rateText      = document.getElementById("rate-text");
const timestampEl   = document.getElementById("timestamp");
const errorDiv      = document.getElementById("error");

// --- Load currencies on page start ---
async function loadCurrencies() {
  try {
    const res  = await fetch(`${API_BASE}/currencies`);
    const data = await res.json();

    data.currencies.forEach(code => {
      fromSelect.add(new Option(code, code));
      toSelect.add(new Option(code, code));
    });

    // Default: USD → SAR (personal touch — you're in Saudi Arabia!)
    fromSelect.value = "USD";
    toSelect.value   = "SAR";
  } catch {
    showError("Could not load currencies. Is the backend running?");
  }
}

// --- Convert ---
async function convert() {
  const amount = parseFloat(amountInput.value);
  if (isNaN(amount) || amount <= 0) {
    showError("Please enter a valid positive amount.");
    return;
  }

  convertBtn.textContent = "Converting...";
  convertBtn.disabled    = true;
  hideMessages();

  try {
    const res = await fetch(`${API_BASE}/convert`, {
      method:  "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        from_currency: fromSelect.value,
        to_currency:   toSelect.value,
        amount:        amount
      })
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Conversion failed.");
    }

    const data = await res.json();
    showResult(data);
  } catch (e) {
    showError(e.message);
  } finally {
    convertBtn.textContent = "Convert";
    convertBtn.disabled    = false;
  }
}

// --- Swap currencies ---
swapBtn.addEventListener("click", () => {
  const temp       = fromSelect.value;
  fromSelect.value = toSelect.value;
  toSelect.value   = temp;
});

// --- Show result ---
function showResult(data) {
  resultText.textContent = `${data.amount} ${data.from_currency} = ${data.converted_amount} ${data.to_currency}`;
  rateText.textContent   = `1 ${data.from_currency} = ${data.rate} ${data.to_currency}`;
  timestampEl.textContent = `Updated: ${new Date(data.timestamp).toLocaleString()}`;
  resultDiv.classList.remove("hidden");
}

function showError(msg) {
  errorDiv.textContent = msg;
  errorDiv.classList.remove("hidden");
}

function hideMessages() {
  resultDiv.classList.add("hidden");
  errorDiv.classList.add("hidden");
}

convertBtn.addEventListener("click", convert);
loadCurrencies();

let historyChart = null;

async function loadHistory() {
  try {
    const res  = await fetch(`${API_BASE}/history?limit=10`);
    const data = await res.json();

    if (data.items.length === 0) return;

    // --- Build chart data ---
    const labels  = data.items.map(i =>
      `${i.from_currency}→${i.to_currency}`
    ).reverse();

    const amounts = data.items.map(i => i.converted_amount).reverse();

    // If chart already exists, destroy it before redrawing
    if (historyChart) historyChart.destroy();

    const ctx = document.getElementById("historyChart").getContext("2d");
    historyChart = new Chart(ctx, {
      type: "bar",
      data: {
        labels,
        datasets: [{
          label: "Converted Amount",
          data: amounts,
          backgroundColor: "rgba(56, 189, 248, 0.6)",
          borderColor: "#38bdf8",
          borderWidth: 1,
          borderRadius: 4,
        }]
      },
      options: {
        responsive: true,
        plugins: {
          legend: { labels: { color: "#94a3b8" } }
        },
        scales: {
          x: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } },
          y: { ticks: { color: "#94a3b8" }, grid: { color: "#334155" } }
        }
      }
    });

    // --- Build list below chart ---
    const listEl = document.getElementById("history-list");
    listEl.innerHTML = data.items.map(i =>
      `<div class="history-item">
        ${i.amount} ${i.from_currency} → ${i.converted_amount} ${i.to_currency}
        &nbsp;·&nbsp; ${new Date(i.created_at).toLocaleString()}
      </div>`
    ).join("");

  } catch (e) {
    console.error("Could not load history:", e);
  }
}

// Reload history after every conversion
const originalConvert = convert;
convertBtn.addEventListener("click", async () => {
  await loadHistory();
});

// Load history when page opens
loadHistory();