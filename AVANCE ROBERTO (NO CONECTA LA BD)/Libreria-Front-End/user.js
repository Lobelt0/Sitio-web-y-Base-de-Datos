const API_BASE = "http://127.0.0.1:8000";

let tiendasCache = {};

// Cargar tiendas
async function cargarTiendas() {
  try {
    const res = await fetch(`${API_BASE}/puntos-venta/`);
    const tiendas = await res.json();
    tiendasCache = {};
    tiendas.forEach(t => tiendasCache[t.id_punto_venta] = t.nombre);
  } catch (e) {
    console.error("Error cargando puntos de venta:", e);
  }
}

// Cargar inventario del usuario
async function cargarInventarioUsuario() {
  const pvId = localStorage.getItem("userPV");

  if (!pvId) {
    alert("Error: No se encontró el Punto de Venta del usuario.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/inventario/?pv=${pvId}`);
    const data = await res.json();

    const tbody = document.getElementById("tabla-inv-user");
    tbody.innerHTML = "";

    data.forEach(item => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${item.libro}</td>
        <td>${item.stock}</td>
        <td><button class="btn" onclick="vender(${item.id_inventario})">Vender</button></td>
      `;
      tbody.appendChild(tr);
    });

  } catch (error) {
    alert("Error cargando inventario");
  }
}

async function vender(idInv) {
  try {
    await fetch(`${API_BASE}/inventario/vender/${idInv}`, { method: "POST" });
    cargarInventarioUsuario();
  } catch (e) {
    alert("Error al registrar venta");
  }
}

// al cargar la página -------------------------
document.addEventListener("DOMContentLoaded", async () => {
  const pvId = localStorage.getItem("userPV");

  console.log("PV ID guardado:", pvId);

  if (!pvId) {
    alert("Error: No se encontró el Punto de Venta del usuario.");
    return;
  }

  const res = await fetch(`${API_BASE}/puntos-venta/${pvId}`);
  const pv = await res.json();

  console.log("PV recibido del backend:", pv);

  document.getElementById("info-pv").textContent =
    `Estás trabajando en: ${pv.nombre}`;
});