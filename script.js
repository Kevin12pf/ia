// ==================== CONFIGURACIÓN ====================

// const API_URL = 'http://localhost:8000/api';
let usuarioActual = null;
let alimentosDisponibles = [];
let medidasActuales = null;

// ==================== UTILIDADES ====================

function mostrarLoading(mostrar = true) {
    document.getElementById('loading').style.display = mostrar ? 'flex' : 'none';
}

function mostrarNotificacion(mensaje, tipo = 'success') {
    console.log(`[${tipo.toUpperCase()}] ${mensaje}`);
    // TODO: Implementar notificación visual
}

// ==================== AUTENTICACIÓN ====================

function switchAuthTab(tab) {
    document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active'));
    document.querySelectorAll('.auth-form').forEach(form => form.classList.remove('active'));
    
    event.target.classList.add('active');
    document.getElementById(`${tab}-form`).classList.add('active');
}

document.getElementById('login-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('login-email').value;
    const password = document.getElementById('login-password').value;
    
    mostrarLoading(true);
    
    try {
        // DATOS DE PRUEBA - Comentar cuando se conecte a API
        if (email === 'test@test.com' && password === '123456') {
            usuarioActual = {
                id: 1,
                email: email,
                nombre: 'Juan Pérez',
                edad: 28,
                objetivo: 'volumen'
            };
            localStorage.setItem('token', 'token_prueba_123');
            mostrarNotificacion('¡Bienvenido!', 'success');
            mostrarPantallaPrincipal();
        } else {
            mostrarNotificacion('Credenciales inválidas (usa test@test.com / 123456)', 'error');
        }
        
        // DESCOMENTAR CUANDO SE CONECTE A API:
        // const response = await fetch(`${API_URL}/auth/login`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ email, password })
        // });
        // const data = await response.json();
        // if (data.success) {
        //     usuarioActual = { id: data.usuario_id, email };
        //     localStorage.setItem('token', data.token);
        //     mostrarNotificacion('¡Bienvenido!', 'success');
        //     mostrarPantallaPrincipal();
        // }
    } catch (error) {
        mostrarNotificacion('Error al conectar', 'error');
        console.error(error);
    } finally {
        mostrarLoading(false);
    }
});

document.getElementById('register-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const email = document.getElementById('register-email').value;
    const fecha_nacimiento = document.getElementById('register-fecha-nacimiento').value;
    const password = document.getElementById('register-password').value;
    
    mostrarLoading(true);
    
    try {
        // DATOS DE PRUEBA - Comentar cuando se conecte a API
        usuarioActual = {
            id: Math.random(),
            email: email,
            nombre: 'Nuevo Usuario',
            fecha_nacimiento: fecha_nacimiento,
            edad: calcularEdad(fecha_nacimiento)
        };
        localStorage.setItem('token', 'token_prueba_' + Math.random());
        mostrarNotificacion('¡Cuenta creada exitosamente!', 'success');
        mostrarModalObjetivo();
        
        // DESCOMENTAR CUANDO SE CONECTE A API:
        // const response = await fetch(`${API_URL}/auth/register`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({ email, fecha_nacimiento, password })
        // });
        // const data = await response.json();
        // if (data.success) {
        //     usuarioActual = data.usuario;
        //     localStorage.setItem('token', data.token);
        //     mostrarNotificacion('¡Cuenta creada exitosamente!', 'success');
        //     mostrarModalObjetivo();
        // }
    } catch (error) {
        mostrarNotificacion('Error al crear la cuenta', 'error');
        console.error(error);
    } finally {
        mostrarLoading(false);
    }
});

function calcularEdad(fechaNacimiento) {
    const hoy = new Date();
    const fecha = new Date(fechaNacimiento);
    let edad = hoy.getFullYear() - fecha.getFullYear();
    const mes = hoy.getMonth() - fecha.getMonth();
    if (mes < 0 || (mes === 0 && hoy.getDate() < fecha.getDate())) {
        edad--;
    }
    return edad;
}

function mostrarPantallaPrincipal() {
    document.getElementById('auth-screen').classList.remove('active');
    document.getElementById('main-screen').classList.add('active');
    actualizarInfoUsuario();
}

function mostrarModalObjetivo() {
    document.getElementById('auth-screen').classList.remove('active');
    document.getElementById('main-screen').classList.add('active');
    document.getElementById('objetivo-modal').style.display = 'flex';
}

async function seleccionarObjetivo(objetivo) {
    mostrarLoading(true);
    
    try {
        // DATOS DE PRUEBA
        usuarioActual.objetivo = objetivo;
        mostrarNotificacion('Objetivo seleccionado', 'success');
        cerrarModalObjetivo();
        
        // DESCOMENTAR CUANDO SE CONECTE A API:
        // const response = await fetch(`${API_URL}/usuario/objetivo`, {
        //     method: 'PUT',
        //     headers: { 
        //         'Content-Type': 'application/json',
        //         'Authorization': `Bearer ${localStorage.getItem('token')}`
        //     },
        //     body: JSON.stringify({ objetivo })
        // });
        // const data = await response.json();
        // if (data.success) {
        //     usuarioActual.objetivo = objetivo;
        //     mostrarNotificacion('Objetivo seleccionado', 'success');
        //     cerrarModalObjetivo();
        // }
    } catch (error) {
        mostrarNotificacion('Error al seleccionar objetivo', 'error');
        console.error(error);
    } finally {
        mostrarLoading(false);
    }
}

function cerrarModalObjetivo() {
    document.getElementById('objetivo-modal').style.display = 'none';
    actualizarInfoUsuario();
}

function actualizarInfoUsuario() {
    if (usuarioActual) {
        document.getElementById('user-name').textContent = usuarioActual.nombre || 'Usuario';
        document.getElementById('user-age').textContent = usuarioActual.edad || '-';
        const objetivoTexto = 
            usuarioActual.objetivo === 'volumen' ? 'Volumen' :
            usuarioActual.objetivo === 'definicion' ? 'Definición' :
            usuarioActual.objetivo === 'recomposicion_corporal' ? 'Recomposición' :
            'Sin objetivo';
        document.getElementById('user-objective').textContent = objetivoTexto;
    }
}

function logout() {
    if (confirm('¿Estás seguro de que deseas cerrar sesión?')) {
        usuarioActual = null;
        alimentosDisponibles = [];
        medidasActuales = null;
        localStorage.removeItem('token');
        
        document.getElementById('main-screen').classList.remove('active');
        document.getElementById('auth-screen').classList.add('active');
        
        document.getElementById('login-form').reset();
        document.getElementById('register-form').reset();
    }
}

// ==================== NAVEGACIÓN DE TABS ====================

function switchTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    document.querySelectorAll('.menu-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    document.getElementById(`${tabName}-tab`).classList.add('active');
    
    // Encontrar y activar el botón correcto
    document.querySelectorAll('.menu-btn').forEach(btn => {
        if (btn.textContent.toLowerCase().includes(tabName.replace('-', ' ')) || 
            btn.onclick.toString().includes(`switchTab('${tabName}')`)) {
            btn.classList.add('active');
        }
    });
}

// ==================== CARGA DE FOTOS ====================

document.getElementById('foto-frontal')?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const preview = document.getElementById('preview-frontal');
            preview.innerHTML = `<img src="${event.target.result}" alt="Foto Frontal">`;
        };
        reader.readAsDataURL(file);
    }
});

document.getElementById('foto-lateral')?.addEventListener('change', (e) => {
    const file = e.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (event) => {
            const preview = document.getElementById('preview-lateral');
            preview.innerHTML = `<img src="${event.target.result}" alt="Foto Lateral">`;
        };
        reader.readAsDataURL(file);
    }
});

async function analizarFotos() {
    const fotoFrontal = document.getElementById('foto-frontal').files[0];
    const fotoLateral = document.getElementById('foto-lateral').files[0];
    
    if (!fotoFrontal || !fotoLateral) {
        mostrarNotificacion('Por favor carga ambas fotos', 'error');
        return;
    }
    
    mostrarLoading(true);
    
    try {
        // DATOS DE PRUEBA
        setTimeout(() => {
            medidasActuales = {
                altura: 1.78,
                peso: 82,
                imc: 25.8,
                porcentaje_grasa: 18
            };
            
            document.getElementById('resultado-altura').textContent = '1.78 m';
            document.getElementById('resultado-peso').textContent = '82 kg';
            document.getElementById('resultado-imc').textContent = '25.8';
            document.getElementById('resultado-grasa').textContent = '18%';
            document.getElementById('medidas-resultado').style.display = 'block';
            
            document.getElementById('user-height').textContent = '1.78 m';
            document.getElementById('user-weight').textContent = '82 kg';
            document.getElementById('user-imc').textContent = '25.8';
            
            mostrarNotificacion('¡Análisis completado!', 'success');
            mostrarLoading(false);
        }, 2000);
        
        // DESCOMENTAR CUANDO SE CONECTE A API:
        // const formData = new FormData();
        // formData.append('imagen_frontal', fotoFrontal);
        // formData.append('imagen_lateral', fotoLateral);
        // formData.append('usuario_id', usuarioActual.id);
        // const response = await fetch(`${API_URL}/medidas/predecir`, {
        //     method: 'POST',
        //     body: formData
        // });
    } catch (error) {
        mostrarNotificacion('Error al analizar', 'error');
        console.error(error);
    }
}

// ==================== ALIMENTOS ====================

function agregarAlimento() {
    const input = document.getElementById('alimento-input');
    const alimento = input.value.trim();
    
    if (!alimento) {
        mostrarNotificacion('Ingresa un alimento', 'error');
        return;
    }
    
    if (alimentosDisponibles.includes(alimento)) {
        mostrarNotificacion('Este alimento ya está en la lista', 'error');
        return;
    }
    
    alimentosDisponibles.push(alimento);
    input.value = '';
    actualizarListaAlimentos();
}

function eliminarAlimento(alimento) {
    alimentosDisponibles = alimentosDisponibles.filter(a => a !== alimento);
    actualizarListaAlimentos();
}

function actualizarListaAlimentos() {
    const lista = document.getElementById('alimentos-lista');
    lista.innerHTML = alimentosDisponibles.map(alimento => `
        <div class="alimento-tag">
            <span>${alimento}</span>
            <button type="button" onclick="eliminarAlimento('${alimento}')">✕</button>
        </div>
    `).join('');
}

document.getElementById('alimento-input')?.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        e.preventDefault();
        agregarAlimento();
    }
});

// ==================== GENERACIÓN DE PLANES ====================

async function generarPlanes() {
    if (!medidasActuales) {
        mostrarNotificacion('Primero debes cargar y analizar tus fotos', 'error');
        return;
    }
    
    if (alimentosDisponibles.length === 0) {
        mostrarNotificacion('Debes agregar al menos un alimento', 'error');
        return;
    }
    
    mostrarLoading(true);
    
    try {
        // DATOS DE PRUEBA
        setTimeout(() => {
            const planNutricion = {
                calorias_diarias: 2500,
                proteina_g: 180,
                carbohidratos_g: 300,
                grasas_g: 80,
                comidas: [
                    {
                        nombre: 'Desayuno',
                        hora: '07:00',
                        calorias: 600,
                        alimentos: ['Huevos', 'Pan integral', 'Jugo de naranja']
                    },
                    {
                        nombre: 'Almuerzo',
                        hora: '12:30',
                        calorias: 800,
                        alimentos: ['Pollo', 'Arroz', 'Brócoli']
                    },
                    {
                        nombre: 'Merienda',
                        hora: '16:00',
                        calorias: 400,
                        alimentos: ['Plátano', 'Frutos secos']
                    },
                    {
                        nombre: 'Cena',
                        hora: '19:00',
                        calorias: 700,
                        alimentos: ['Salmón', 'Batata', 'Espinaca']
                    }
                ]
            };
            
            const planEjercicios = {
                intensidad: 'Moderada-Alta',
                dias_semana: [
                    {
                        dia: 'Lunes',
                        grupo_muscular: 'Pecho y Tríceps',
                        ejercicios: [
                            { nombre: 'Press de banca', series: 4, repeticiones: '8-10', descanso: 90 },
                            { nombre: 'Fondos', series: 3, repeticiones: '10-12', descanso: 60 }
                        ]
                    },
                    {
                        dia: 'Martes',
                        grupo_muscular: 'Espalda y Bíceps',
                        ejercicios: [
                            { nombre: 'Dominadas', series: 4, repeticiones: '8-10', descanso: 90 },
                            { nombre: 'Remo', series: 3, repeticiones: '10-12', descanso: 60 }
                        ]
                    },
                    {
                        dia: 'Miércoles',
                        grupo_muscular: 'Descanso',
                        ejercicios: []
                    },
                    {
                        dia: 'Jueves',
                        grupo_muscular: 'Piernas',
                        ejercicios: [
                            { nombre: 'Sentadillas', series: 4, repeticiones: '8-10', descanso: 90 },
                            { nombre: 'Prensa de piernas', series: 3, repeticiones: '10-12', descanso: 60 }
                        ]
                    },
                    {
                        dia: 'Viernes',
                        grupo_muscular: 'Hombros',
                        ejercicios: [
                            { nombre: 'Press militar', series: 4, repeticiones: '8-10', descanso: 90 }
                        ]
                    },
                    {
                        dia: 'Sábado',
                        grupo_muscular: 'Descanso',
                        ejercicios: []
                    },
                    {
                        dia: 'Domingo',
                        grupo_muscular: 'Descanso',
                        ejercicios: []
                    }
                ]
            };
            
            mostrarPlanNutricion(planNutricion);
            mostrarPlanEjercicios(planEjercicios);
            mostrarNotificacion('¡Planes generados exitosamente!', 'success');
            switchTab('nutricion');
            mostrarLoading(false);
        }, 2000);
        
        // DESCOMENTAR CUANDO SE CONECTE A API:
        // const response = await fetch(`${API_URL}/planes/generar`, {
        //     method: 'POST',
        //     headers: { 'Content-Type': 'application/json' },
        //     body: JSON.stringify({...})
        // });
    } catch (error) {
        mostrarNotificacion('Error al generar planes', 'error');
        console.error(error);
    } finally {
        mostrarLoading(false);
    }
}

function mostrarPlanNutricion(plan) {
    const contenido = document.getElementById('nutricion-contenido');
    
    let html = `
        <div class="macros-summary">
            <div class="macro-item">
                <h4>Calorías Diarias</h4>
                <p>${plan.calorias_diarias.toFixed(0)}</p>
            </div>
            <div class="macro-item">
                <h4>Proteína</h4>
                <p>${plan.proteina_g.toFixed(1)}g</p>
            </div>
            <div class="macro-item">
                <h4>Carbohidratos</h4>
                <p>${plan.carbohidratos_g.toFixed(1)}g</p>
            </div>
            <div class="macro-item">
                <h4>Grasas</h4>
                <p>${plan.grasas_g.toFixed(1)}g</p>
            </div>
        </div>
    `;
    
    plan.comidas.forEach(comida => {
        html += `
            <div class="comida-card">
                <div class="comida-header">
                    <span class="comida-nombre">${comida.nombre}</span>
                    <span class="comida-hora">${comida.hora}</span>
                </div>
                <div class="comida-calorias">
                    Calorías: ${comida.calorias.toFixed(0)} kcal
                </div>
                <div class="alimentos-comida">
                    ${comida.alimentos.map(alimento => 
                        `<span class="alimento-item">${alimento}</span>`
                    ).join('')}
                </div>
            </div>
        `;
    });
    
    contenido.innerHTML = html;
}

function mostrarPlanEjercicios(plan) {
    const contenido = document.getElementById('ejercicios-contenido');
    
    let html = `<div style="margin-bottom: 20px; padding: 15px; background: linear-gradient(135deg, #06A77D 0%, #048A5C 100%); color: white; border-radius: 8px;">
        <strong>Intensidad del Plan:</strong> ${plan.intensidad}
    </div>`;
    
    plan.dias_semana.forEach(dia => {
        if (dia.ejercicios.length === 0) {
            html += `
                <div class="dia-card">
                    <div class="dia-header">
                        <span class="dia-nombre">${dia.dia}</span>
                        <span class="grupo-muscular">Descanso</span>
                    </div>
                    <p style="color: #999; text-align: center; padding: 20px;">Día de descanso - Recuperación</p>
                </div>
            `;
        } else {
            html += `
                <div class="dia-card">
                    <div class="dia-header">
                        <span class="dia-nombre">${dia.dia}</span>
                        <span class="grupo-muscular">${dia.grupo_muscular}</span>
                    </div>
            `;
            
            dia.ejercicios.forEach(ejercicio => {
                html += `
                    <div class="ejercicio-item">
                        <div class="ejercicio-nombre">${ejercicio.nombre}</div>
                        <div class="ejercicio-detalles">
                            <span class="ejercicio-detalle">
                                <strong>Series:</strong> ${ejercicio.series}
                            </span>
                            <span class="ejercicio-detalle">
                                <strong>Reps:</strong> ${ejercicio.repeticiones}
                            </span>
                            <span class="ejercicio-detalle">
                                <strong>Descanso:</strong> ${ejercicio.descanso}s
                            </span>
                        </div>
                    </div>
                `;
            });
            
            html += `</div>`;
        }
    });
    
    contenido.innerHTML = html;
}

// ==================== INICIALIZACIÓN ====================

document.addEventListener('DOMContentLoaded', () => {
    const token = localStorage.getItem('token');
    // TODO: Restaurar sesión cuando se conecte con API
});
