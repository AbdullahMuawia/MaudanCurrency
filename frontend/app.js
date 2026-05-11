const API_BASE = "http://localhost:8000/api";

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