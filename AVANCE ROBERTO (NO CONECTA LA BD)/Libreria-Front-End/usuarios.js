const API_BASE = "http://127.0.0.1:8000";

async function cargarUsuarios(q = "") {
  const tbody = document.getElementById("tabla-usuarios");
  tbody.innerHTML = "<tr><td colspan='6'>Cargando...</td></tr>";

  let url = `${API_BASE}/usuarios/`;
  if (q) url += `?q=${encodeURIComponent(q)}`;

  const res = await fetch(url);
  const data = await res.json();

  tbody.innerHTML = "";

  if (!data.length) {
    tbody.innerHTML = "<tr><td colspan='6'>No hay usuarios registrados</td></tr>";
    return;
  }

  data.forEach(u => {
    const pv = u.punto_venta_id ?? "—";

    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${u.id_usuario}</td>
      <td>${u.nombre}</td>
      <td>${u.email}</td>
      <td>${u.rol}</td>
      <td>${pv}</td>
      <td>
        <a href="#" class="link" onclick="abrirModalEditar(${u.id_usuario})">Editar</a>
        <a href="#" class="link" onclick="eliminarUsuario(${u.id_usuario})">Eliminar</a>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// eliminar usuario
async function eliminarUsuario(id) {
  if (!confirm("¿Eliminar usuario?")) return;

const res = await fetch(`${API_BASE}/usuarios/login`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ email, contrasena })
});

const data = await res.json();

// Guardar rol
localStorage.setItem("userRole", data.role);

// 🔥 GUARDAR PUNTO DE VENTA DEL VENDEDOR
if (data.role === "vendedor") {
  localStorage.setItem("userPV", data.punto_venta_id);
}


document.addEventListener("DOMContentLoaded", () => {
  cargarUsuarios();

  const formFiltro = document.getElementById("filterFormUsuarios");
  formFiltro.addEventListener("submit", e => {
    e.preventDefault();
    cargarUsuarios(formFiltro.q.value.trim());
  });
});}
