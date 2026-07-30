# 📚 Manual de Usuario - CoworkSpace KC

## 🎯 ¿Qué es CoworkSpace KC?

CoworkSpace KC es un **sistema de gestión para espacios de coworking** que permite administrar:
- 🏢 Empresas clientes
- 👥 Miembros de cada empresa
- 🚪 Salas de reunión
- 💼 Escritorios dedicados
- 📅 Reservas de espacios
- 🎉 Eventos del coworking
- 💰 Facturación

---

## 🔐 Tipos de Usuario

### 1. **Usuario Regular** (Miembro de Empresa)
- ✅ Ver sus propias reservas
- ✅ Crear nuevas reservas
- ✅ Ver eventos disponibles
- ✅ Ver información de su empresa
- ❌ NO puede ver datos de otras empresas
- ❌ NO puede acceder a reportes

### 2. **Superusuario** (Administrador)
- ✅ Ver TODAS las empresas y datos
- ✅ Crear, editar, eliminar cualquier registro
- ✅ Acceder a reportes y estadísticas
- ✅ Gestionar facturación
- ✅ Panel de administración Django

---

## 🚀 Flujo de Uso del Sistema

### **FLUJO COMPLETO:**

```
1. REGISTRO/LOGIN
   ↓
2. CREAR EMPRESA CLIENTE
   ↓
3. AGREGAR MIEMBROS A LA EMPRESA
   ↓
4. VER ESPACIOS DISPONIBLES (Salas/Escritorios)
   ↓
5. HACER RESERVAS EN EL CALENDARIO
   ↓
6. PARTICIPAR EN EVENTOS
   ↓
7. GENERAR FACTURA (Admin)
   ↓
8. VER REPORTES (Admin)
```

---

## 📋 Módulos del Sistema

### 1️⃣ **EMPRESAS CLIENTES**

**¿Qué es?**
Una empresa cliente es una organización que contrata espacios en el coworking.

**Información que se guarda:**
- 🏢 Nombre de la empresa
- 📄 RUC (Registro Único de Contribuyentes)
- 📧 Email de contacto
- 📞 Teléfono
- 📍 Dirección
- 🖼️ Logo (opcional)
- 💳 Plan contratado:
  - **Básico:** Acceso limitado
  - **Profesional:** Más beneficios
  - **Empresarial:** Acceso completo
- ✅ Estado: Activo/Inactivo

**Funciones:**
- ➕ **Nueva Empresa:** Registrar una nueva empresa cliente
- 👁️ **Listar Empresas:** Ver todas las empresas registradas
- ✏️ **Editar:** Modificar datos de la empresa
- 🗑️ **Eliminar:** Eliminar empresa (con confirmación)
- 👥 **Ver Miembros:** Ver los miembros de cada empresa

**Acceso:**
- Usuarios regulares: Solo ven su propia empresa
- Admin: Ve todas las empresas

---

### 2️⃣ **MIEMBROS**

**¿Qué es?**
Los miembros son las personas que trabajan para una empresa cliente.

**Información que se guarda:**
- 👤 Nombre completo
- 📧 Email
- 📞 Teléfono
- 🆔 Cédula de identidad
- 💼 Cargo en la empresa
- 📸 Foto (opcional)
- 🏢 Empresa a la que pertenece
- 📅 Fecha de ingreso
- ✅ Estado: Activo/Inactivo

**Funciones:**
- ➕ **Nuevo Miembro:** Agregar miembro a una empresa
- 👁️ **Listar Miembros:** Ver miembros de una empresa
- ✏️ **Editar:** Actualizar datos del miembro
- 🗑️ **Eliminar:** Eliminar miembro

**Acceso:**
- Usuarios regulares: Solo ven miembros de su empresa
- Admin: Ve todos los miembros

---

### 3️⃣ **SALAS DE REUNIÓN**

**¿Qué es?**
Espacios cerrados para reuniones, capacitaciones o conferencias.

**Información que se guarda:**
- 🚪 Nombre de la sala
- 👥 Capacidad (número de personas)
- 📐 Metros cuadrados
- 🏢 Piso donde se encuentra
- 💵 Precio por hora
- 🎥 Equipamiento:
  - **Básico:** Mesa y sillas
  - **Ejecutivo:** + Proyector
  - **Premium:** + TV, videoconferencia, pizarra
- 🖼️ Foto de la sala
- ✅ Estado: Activa/Inactiva

**Funciones:**
- ➕ **Nueva Sala:** Registrar sala de reunión
- 👁️ **Listar Salas:** Ver todas las salas disponibles
- ✏️ **Editar:** Modificar información de la sala
- 🗑️ **Eliminar:** Eliminar sala

**Precio promedio:** $25-$50 por hora

---

### 4️⃣ **ESCRITORIOS DEDICADOS**

**¿Qué es?**
Espacios de trabajo fijos asignados a un miembro específico.

**Información que se guarda:**
- 🔢 Código del escritorio (ej: "ESC-101")
- 🏢 Piso
- 📍 Posición en el piso
- 💵 Precio mensual
- 📦 Tipo:
  - **Individual:** 1 persona
  - **Doble:** 2 personas  
  - **Triple:** 3 personas
- ✅ Estado:
  - **Disponible:** Sin asignar
  - **Ocupado:** Asignado a un miembro
  - **Mantenimiento:** No disponible
- 👤 Miembro asignado (si está ocupado)

**Funciones:**
- ➕ **Nuevo Escritorio:** Registrar escritorio
- 👁️ **Listar Escritorios:** Ver todos los escritorios
- 🗺️ **Mapa Interactivo:** Ver escritorios en un mapa visual (jQuery UI Draggable)
- ✏️ **Editar:** Modificar información
- 🗑️ **Eliminar:** Eliminar escritorio

**Precio promedio:** $150-$300 por mes

---

### 5️⃣ **RESERVAS**

**¿Qué es?**
Solicitudes para usar una sala de reunión en fecha y hora específica.

**Información que se guarda:**
- 👤 Miembro que reserva
- 🚪 Sala reservada
- 📅 Fecha de la reserva
- ⏰ Hora de inicio
- ⏰ Hora de fin
- 👥 Número de asistentes
- 📝 Propósito de la reserva
- 💵 Costo total (calculado automáticamente)
- ✅ Estado:
  - **Pendiente:** En espera de confirmación
  - **Confirmada:** Aprobada
  - **Cancelada:** Cancelada
  - **Completada:** Ya se realizó

**Funciones:**
- ➕ **Nueva Reserva:** Crear reserva de sala
- 📅 **Calendario:** Ver reservas en FullCalendar (vista mensual/semanal/diaria)
- 👁️ **Listar Reservas:** Ver todas las reservas
- ✏️ **Editar:** Modificar reserva (solo si está pendiente)
- 🗑️ **Cancelar:** Cancelar reserva

**Cálculo automático:**
```
Costo = (Precio/hora de la sala) × (Número de horas)
```

**Vista de Calendario:**
- 📅 Mes completo
- 📆 Semana
- 📋 Día
- 📝 Lista

---

### 6️⃣ **EVENTOS**

**¿Qué es?**
Actividades organizadas por el coworking para la comunidad.

**Información que se guarda:**
- 🎉 Título del evento
- 📝 Descripción
- 🏢 Empresa organizadora
- 📅 Fecha del evento
- ⏰ Hora de inicio
- ⏰ Hora de fin
- 🚪 Sala donde se realiza (opcional)
- 👥 Capacidad máxima
- 🖼️ Foto del evento
- 🎯 Tipo:
  - **Networking:** Eventos de conexión
  - **Capacitación:** Talleres y cursos
  - **Conferencia:** Charlas y presentaciones
  - **Social:** Eventos recreativos
- 🌐 Visibilidad:
  - **Público:** Todos pueden ver y asistir
  - **Privado:** Solo miembros del coworking

**Funciones:**
- ➕ **Nuevo Evento:** Crear evento (Admin)
- 👁️ **Listar Eventos:** Ver eventos próximos
- 📋 **Ver Detalles:** Información completa del evento
- ✏️ **Editar:** Modificar evento
- 🗑️ **Eliminar:** Eliminar evento (Admin)

---

### 7️⃣ **FACTURAS**

**¿Qué es?**
Documentos de cobro generados para las empresas clientes.

**Información que se guarda:**
- 🔢 Número de factura (generado automáticamente)
- 🏢 Empresa cliente
- 📅 Fecha de emisión
- 📅 Fecha de vencimiento
- 💵 Subtotal
- 💵 IVA (15% en Ecuador)
- 💵 Total
- 📝 Detalles de la factura
- 💳 Método de pago:
  - Efectivo
  - Transferencia
  - Tarjeta
  - Cheque
- ✅ Estado:
  - **Pendiente:** No pagada
  - **Pagada:** Cobrada
  - **Vencida:** Pasó la fecha de vencimiento
  - **Anulada:** Cancelada

**Funciones:**
- ➕ **Nueva Factura:** Generar factura (Admin)
- 👁️ **Listar Facturas:** Ver todas las facturas
- 📄 **Ver PDF:** Descargar factura en PDF
- ✏️ **Editar:** Modificar factura (solo si está pendiente)
- 🗑️ **Anular:** Anular factura

**Cálculo automático:**
```
IVA = Subtotal × 0.15
Total = Subtotal + IVA
```

---

### 8️⃣ **REPORTES** (Solo Admin)

**¿Qué son?**
Informes estadísticos para tomar decisiones.

#### **📊 Reporte 1: Panel Principal**
- 📈 Total de empresas activas
- 👥 Total de miembros
- 🚪 Salas disponibles
- 💼 Escritorios ocupados
- 💰 Ingresos del mes

#### **📊 Reporte 2: Ocupación de Espacios**
Gráficos con Chart.js:
- 🥧 **Gráfico Circular:** Escritorios ocupados vs disponibles
- 📊 **Gráfico de Barras:** Ocupación por piso

#### **📊 Reporte 3: Facturación**
Gráficos con Chart.js:
- 📊 **Gráfico de Barras:** Facturación por empresa
- 🥧 **Gráfico Circular:** Estados de facturas (pagadas/pendientes/vencidas)
- 📊 **Gráfico Horizontal:** Top 5 empresas por ingresos

**Funciones:**
- 📥 **Exportar a Excel:** Descargar datos en Excel
- 📄 **Exportar a PDF:** Generar PDF del reporte

---

## 🎨 Características Especiales

### 1. **📅 Calendario Interactivo (FullCalendar)**
- Vista de reservas en formato calendario
- Crear reserva haciendo clic en una fecha
- Arrastrar y soltar para reprogramar (drag & drop)
- Filtrar por sala
- Colores por estado de reserva

### 2. **🗺️ Mapa Interactivo de Escritorios (jQuery UI)**
- Ver distribución de escritorios por piso
- Arrastrar escritorios para reposicionarlos
- Códigos de color:
  - 🟢 Verde: Disponible
  - 🔴 Rojo: Ocupado
  - 🟡 Amarillo: Mantenimiento

### 3. **📊 Tablas con DataTables**
Todas las tablas tienen:
- 🔍 Búsqueda en tiempo real
- 📄 Paginación
- 🔤 Ordenamiento por columnas
- 📥 Exportar a:
  - Excel
  - PDF
  - CSV
  - Copiar al portapapeles

### 4. **⌨️ Atajos de Teclado (Hotkeys.js)**
- `Ctrl + R`: Nueva reserva rápida
- `Ctrl + D`: Ir al dashboard
- (Funciona solo en página de inicio cuando estás logueado)

### 5. **🎓 Tour Guiado (Driver.js)**
- Primera vez que entras, te muestra un tour del sistema
- Explica cada sección paso a paso
- Se ejecuta solo la primera vez (guarda en localStorage)

### 6. **📸 Subida de Imágenes (Bootstrap FileInput)**
- Vista previa de imágenes
- Arrastrar y soltar
- Validación de formato (solo imágenes)
- Límite de tamaño: 5MB

### 7. **🎨 Validaciones en Formularios**
- Validación en tiempo real con JavaScript
- Mensajes de error amigables
- No permite enviar formularios vacíos
- Valida formatos (email, teléfono, RUC)

### 8. **✅ Confirmaciones con SweetAlert2**
- Confirmación antes de eliminar
- Mensajes de éxito/error bonitos
- Alertas animadas

---

## 🔄 Flujos Detallados

### **FLUJO 1: Registrar Nueva Empresa**

1. Click en menú **"Empresas"**
2. Click en botón **"+ Nueva Empresa"**
3. Llenar formulario:
   - Nombre (obligatorio)
   - RUC (obligatorio, 13 dígitos)
   - Email (obligatorio)
   - Teléfono
   - Dirección
   - Plan (seleccionar: Básico/Profesional/Empresarial)
   - Logo (opcional, imagen)
4. Click en **"Guardar"**
5. Sistema muestra mensaje de confirmación
6. Redirecciona a listado de empresas

---

### **FLUJO 2: Agregar Miembro a Empresa**

1. En listado de **Empresas**
2. Click en botón **"👥 [número]"** (Ver Miembros)
3. Click en **"+ Nuevo Miembro"**
4. Llenar formulario:
   - Nombre completo (obligatorio)
   - Email (obligatorio)
   - Cédula (obligatorio, 10 dígitos)
   - Teléfono
   - Cargo
   - Foto (opcional)
5. Click en **"Guardar"**
6. Miembro queda asociado a la empresa

---

### **FLUJO 3: Crear Reserva de Sala**

#### **Opción A: Desde el Calendario**
1. Click en menú **"Reservas"**
2. Se abre el calendario FullCalendar
3. Click en una fecha vacía
4. Se abre formulario modal
5. Seleccionar:
   - Sala
   - Hora inicio
   - Hora fin
   - Número de asistentes
   - Propósito
6. Click en **"Guardar"**
7. Sistema calcula el costo automáticamente
8. Reserva aparece en el calendario

#### **Opción B: Desde el Listado**
1. Click en menú **"Reservas"**
2. Click en pestaña **"Lista"** o botón **"+ Nueva Reserva"**
3. Llenar formulario completo
4. Click en **"Guardar"**

---

### **FLUJO 4: Generar Factura (Admin)**

1. Click en menú **"Facturas"**
2. Click en **"+ Nueva Factura"**
3. Seleccionar:
   - Empresa cliente
   - Fecha de emisión
   - Fecha de vencimiento
   - Método de pago
4. Agregar detalles:
   - Descripción del servicio
   - Subtotal
5. Sistema calcula automáticamente:
   - IVA (15%)
   - Total
6. Click en **"Guardar"**
7. Factura queda en estado **"Pendiente"**
8. Opción de descargar PDF

---

### **FLUJO 5: Ver Reportes (Admin)**

1. Click en menú **"Reportes"**
2. Ver dashboard con estadísticas generales
3. Click en reportes específicos:
   - **"Reporte de Ocupación"** → Gráficos de escritorios
   - **"Reporte de Facturación"** → Gráficos de ingresos
4. Exportar datos:
   - Click en botón **"Excel"** o **"PDF"**
   - Descarga automáticamente

---

## 🎯 Casos de Uso Comunes

### **CASO 1: Nueva empresa se registra**
```
1. Admin registra la empresa
2. Admin crea primer miembro (gerente)
3. Miembro hace login
4. Miembro reserva una sala para reunión
5. Admin genera factura mensual
```

### **CASO 2: Empresa necesita escritorio**
```
1. Miembro revisa escritorios disponibles
2. Miembro ve mapa interactivo
3. Admin asigna escritorio al miembro
4. Admin genera factura de alquiler mensual
```

### **CASO 3: Evento de networking**
```
1. Admin crea evento "Networking Night"
2. Marca como público
3. Todos los miembros ven el evento
4. Admin reserva sala grande para el evento
5. Evento aparece en el calendario
```

---

## 📱 Acceso al Sistema

### **URL Local:**
```
http://localhost:8000/
```

### **Rutas principales:**
- `/` → Página de inicio
- `/login/` → Iniciar sesión
- `/registro/` → Registrarse
- `/dashboard/` → Panel de control
- `/empresas/` → Listado de empresas
- `/salas/` → Salas de reunión
- `/escritorios/` → Escritorios dedicados
- `/reservas/calendario/` → Calendario de reservas
- `/eventos/` → Eventos del coworking
- `/facturas/` → Gestión de facturas
- `/reportes/` → Reportes estadísticos
- `/admin/` → Panel admin de Django

---

## 🔒 Seguridad

### **Autenticación:**
- Todas las vistas requieren `@login_required`
- No puedes acceder sin estar logueado

### **Permisos:**
- Usuarios regulares solo ven sus datos
- Admin ve todo
- Reportes solo para superusuarios

### **Validaciones:**
- No se pueden duplicar RUCs
- No se pueden duplicar cédulas
- Fechas de reserva deben ser futuras
- Horas de fin deben ser después de inicio

---

## 🎨 Paleta de Colores

- **Principal:** Azul medio `#4A6785`
- **Oscuro:** Azul oscuro `#2D4A64`
- **Muy oscuro:** `#1A2E42`
- **Claro:** Azul claro `#6B89A8`
- **Muy claro:** `#B4C5D8`
- **Texto en fondos oscuros:** Blanco `#ffffff`
- **Texto en fondos claros:** Azul muy oscuro `#1A2E42`

---

## 💡 Tips de Uso

1. **Usa los atajos de teclado** para ser más rápido
2. **Filtra las tablas** usando la barra de búsqueda
3. **Exporta datos** cuando necesites informes
4. **Revisa el calendario** antes de reservar
5. **Actualiza el estado** de las reservas después de usarlas
6. **Marca las facturas como pagadas** cuando se cobren
7. **Usa el mapa interactivo** para ver escritorios disponibles
8. **Revisa los eventos** regularmente

---

## ❓ Preguntas Frecuentes (FAQ)

**P: ¿Puedo ver datos de otras empresas?**
R: No, solo si eres administrador.

**P: ¿Puedo cancelar una reserva?**
R: Sí, pero solo si está en estado "Pendiente" o "Confirmada".

**P: ¿Cuánto cuesta una sala por hora?**
R: Depende del equipamiento. Desde $25 (básica) hasta $50 (premium).

**P: ¿Los escritorios son mensuales?**
R: Sí, se alquilan por mes completo.

**P: ¿Cómo se calcula el IVA?**
R: Automáticamente, es el 15% del subtotal.

**P: ¿Puedo mover un escritorio en el mapa?**
R: Sí, arrastra y suelta (solo admin).

**P: ¿Los eventos son gratuitos?**
R: Depende del evento, pero generalmente sí para miembros.

---

## 🚀 Próximos Pasos

### **Para probar el sistema:**

1. **Iniciar el servidor:**
```bash
python manage.py runserver
```

2. **Crear superusuario** (si no existe):
```bash
python manage.py createsuperuser
```

3. **Acceder al sistema:**
```
http://localhost:8000/
```

4. **Probar en este orden:**
   1. ✅ Registrar una empresa
   2. ✅ Agregar miembros
   3. ✅ Ver/crear salas
   4. ✅ Ver/crear escritorios
   5. ✅ Hacer una reserva en el calendario
   6. ✅ Crear un evento
   7. ✅ Generar una factura
   8. ✅ Ver reportes

---

## 📞 Soporte

**Desarrollador:** KC  
**Versión:** 2.0  
**Fecha:** Enero 2026  
**Base de Datos:** `coworkspace_kc.db` (SQLite)

---

**¡Listo para usar! 🎉**


---

## 🧪 DATOS DE PRUEBA PARA TESTING

### 📋 **Guía de Pruebas Paso a Paso**

Usa estos datos para probar todas las funcionalidades del sistema de forma organizada.

---

## 🏢 EMPRESAS CLIENTES (5 Empresas)

### **Empresa 1: TechSolutions Cía. Ltda.**
```
Nombre: TechSolutions Cía. Ltda.
RUC: 1792345678001
Email: contacto@techsolutions.com.ec
Teléfono: 0987654321
Dirección: Av. Eloy Alfaro y Amazonas, Edificio Torre Central, Piso 5, Latacunga
Plan: Empresarial
Logo: (opcional - buscar logo de empresa tech)
Estado: Activo
```

**Descripción:** Empresa de desarrollo de software y consultoría tecnológica.

---

### **Empresa 2: Marketing Digital Pro**
```
Nombre: Marketing Digital Pro
RUC: 1791234567001
Email: info@marketingdigitalpro.ec
Teléfono: 0998765432
Dirección: Calle Quito 45-23 y Guayaquil, Latacunga
Plan: Profesional
Logo: (opcional)
Estado: Activo
```

**Descripción:** Agencia de marketing digital y redes sociales.

---

### **Empresa 3: EcoVerde S.A.**
```
Nombre: EcoVerde S.A.
RUC: 1790987654001
Email: contacto@ecoverde.com.ec
Teléfono: 0976543210
Dirección: Av. Unidad Nacional Km 2, Parque Empresarial, Latacunga
Plan: Básico
Logo: (opcional - logo ecológico)
Estado: Activo
```

**Descripción:** Empresa de consultoría ambiental y sostenibilidad.

---

### **Empresa 4: Diseño Creativo Studio**
```
Nombre: Diseño Creativo Studio
RUC: 1793456789001
Email: hola@disenocreativo.ec
Teléfono: 0965432109
Dirección: Calle Salcedo 12-34, Centro Histórico, Latacunga
Plan: Profesional
Logo: (opcional - logo creativo)
Estado: Activo
```

**Descripción:** Estudio de diseño gráfico y branding.

---

### **Empresa 5: LegalConsult Abogados**
```
Nombre: LegalConsult Abogados
RUC: 1794567890001
Email: contacto@legalconsult.ec
Teléfono: 0954321098
Dirección: Av. Amazonas y Patria, Edificio Corporativo, Piso 3, Latacunga
Plan: Empresarial
Logo: (opcional - logo legal)
Estado: Activo
```

**Descripción:** Firma de abogados especializada en derecho corporativo.

---

## 👥 MIEMBROS (3 por empresa = 15 miembros)

### **MIEMBROS DE TECHSOLUTIONS:**

#### Miembro 1:
```
Nombre Completo: Carlos Andrés Morales Vega
Email: carlos.morales@techsolutions.com.ec
Cédula: 1750123456
Teléfono: 0987654321
Cargo: CEO y Fundador
Empresa: TechSolutions Cía. Ltda.
Fecha Ingreso: 01/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 2:
```
Nombre Completo: María Fernanda López García
Email: maria.lopez@techsolutions.com.ec
Cédula: 1750234567
Teléfono: 0987654322
Cargo: Gerente de Proyectos
Empresa: TechSolutions Cía. Ltda.
Fecha Ingreso: 15/02/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 3:
```
Nombre Completo: Juan Pablo Sánchez Torres
Email: juan.sanchez@techsolutions.com.ec
Cédula: 1750345678
Teléfono: 0987654323
Cargo: Desarrollador Senior
Empresa: TechSolutions Cía. Ltda.
Fecha Ingreso: 01/03/2024
Foto: (opcional)
Estado: Activo
```

---

### **MIEMBROS DE MARKETING DIGITAL PRO:**

#### Miembro 4:
```
Nombre Completo: Ana Cristina Romero Flores
Email: ana.romero@marketingdigitalpro.ec
Cédula: 1750456789
Teléfono: 0998765432
Cargo: Directora de Marketing
Empresa: Marketing Digital Pro
Fecha Ingreso: 10/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 5:
```
Nombre Completo: Diego Alejandro Castro Ruiz
Email: diego.castro@marketingdigitalpro.ec
Cédula: 1750567890
Teléfono: 0998765433
Cargo: Community Manager
Empresa: Marketing Digital Pro
Fecha Ingreso: 20/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 6:
```
Nombre Completo: Sofía Isabel Mendoza Álvarez
Email: sofia.mendoza@marketingdigitalpro.ec
Cédula: 1750678901
Teléfono: 0998765434
Cargo: Diseñadora Gráfica
Empresa: Marketing Digital Pro
Fecha Ingreso: 01/02/2024
Foto: (opcional)
Estado: Activo
```

---

### **MIEMBROS DE ECOVERDE:**

#### Miembro 7:
```
Nombre Completo: Roberto Carlos Gutiérrez Pérez
Email: roberto.gutierrez@ecoverde.com.ec
Cédula: 1750789012
Teléfono: 0976543210
Cargo: Consultor Ambiental Senior
Empresa: EcoVerde S.A.
Fecha Ingreso: 05/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 8:
```
Nombre Completo: Laura Patricia Díaz Morales
Email: laura.diaz@ecoverde.com.ec
Cédula: 1750890123
Teléfono: 0976543211
Cargo: Ingeniera Ambiental
Empresa: EcoVerde S.A.
Fecha Ingreso: 15/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 9:
```
Nombre Completo: Andrés Felipe Vargas Silva
Email: andres.vargas@ecoverde.com.ec
Cédula: 1750901234
Teléfono: 0976543212
Cargo: Asistente de Proyectos
Empresa: EcoVerde S.A.
Fecha Ingreso: 01/02/2024
Foto: (opcional)
Estado: Activo
```

---

### **MIEMBROS DE DISEÑO CREATIVO STUDIO:**

#### Miembro 10:
```
Nombre Completo: Valentina Alejandra Rojas Herrera
Email: valentina.rojas@disenocreativo.ec
Cédula: 1751012345
Teléfono: 0965432109
Cargo: Directora Creativa
Empresa: Diseño Creativo Studio
Fecha Ingreso: 01/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 11:
```
Nombre Completo: Sebastián Mateo Cruz Jiménez
Email: sebastian.cruz@disenocreativo.ec
Cédula: 1751123456
Teléfono: 0965432110
Cargo: Ilustrador Digital
Empresa: Diseño Creativo Studio
Fecha Ingreso: 10/01/2024
Foto: (opcional)
Estado: Activo
```

#### Miembro 12:
```
Nombre Completo: Camila Andrea Ortiz Navarro
Email: camila.ortiz@disenocreativo.ec
Cédula: 1751234567
Teléfono: 0965432111
Cargo: Motion Designer
Empresa: Diseño Creativo Studio
Fecha Ingreso: 20/01/2024
Foto: (opcional)
Estado: Activo
```

---

### **MIEMBROS DE LEGALCONSULT:**

#### Miembro 13:
```
Nombre Completo: Dr. Fernando José Ramírez Castillo
Email: fernando.ramirez@legalconsult.ec
Cédula: 1751345678
Teléfono: 0954321098
Cargo: Socio Principal
Empresa: LegalConsult Abogados
Fecha Ingreso: 01/12/2023
Foto: (opcional)
Estado: Activo
```

#### Miembro 14:
```
Nombre Completo: Dra. Patricia Elena Montenegro Ríos
Email: patricia.montenegro@legalconsult.ec
Cédula: 1751456789
Teléfono: 0954321099
Cargo: Abogada Corporativa
Empresa: LegalConsult Abogados
Fecha Ingreso: 15/12/2023
Foto: (opcional)
Estado: Activo
```

#### Miembro 15:
```
Nombre Completo: Gabriel Esteban Paredes Luna
Email: gabriel.paredes@legalconsult.ec
Cédula: 1751567890
Teléfono: 0954321100
Cargo: Asistente Legal
Empresa: LegalConsult Abogados
Fecha Ingreso: 01/01/2024
Foto: (opcional)
Estado: Activo
```

---

## 🚪 SALAS DE REUNIÓN (6 Salas)

### **Sala 1: Sala Innovación**
```
Nombre: Sala Innovación
Capacidad: 8 personas
Metros Cuadrados: 25.50
Piso: 1
Precio por Hora: $30.00
Equipamiento: Premium (Proyector, TV 55", Videoconferencia, Pizarra Interactiva)
Foto: (opcional)
Estado: Activa
```

---

### **Sala 2: Sala Ejecutiva**
```
Nombre: Sala Ejecutiva
Capacidad: 12 personas
Metros Cuadrados: 35.00
Piso: 2
Precio por Hora: $45.00
Equipamiento: Premium (Proyector, TV 65", Videoconferencia, Pizarra, Sistema de Audio)
Foto: (opcional)
Estado: Activa
```

---

### **Sala 3: Sala Colaborativa**
```
Nombre: Sala Colaborativa
Capacidad: 6 personas
Metros Cuadrados: 20.00
Piso: 1
Precio por Hora: $25.00
Equipamiento: Ejecutivo (Proyector, Pizarra, TV 43")
Foto: (opcional)
Estado: Activa
```

---

### **Sala 4: Sala Estrategia**
```
Nombre: Sala Estrategia
Capacidad: 10 personas
Metros Cuadrados: 30.00
Piso: 2
Precio por Hora: $35.00
Equipamiento: Ejecutivo (Proyector, TV 50", Pizarra)
Foto: (opcional)
Estado: Activa
```

---

### **Sala 5: Sala Meeting Point**
```
Nombre: Sala Meeting Point
Capacidad: 4 personas
Metros Cuadrados: 15.00
Piso: 1
Precio por Hora: $20.00
Equipamiento: Básico (Mesa, Sillas, Pizarra pequeña)
Foto: (opcional)
Estado: Activa
```

---

### **Sala 6: Sala Auditorio**
```
Nombre: Sala Auditorio
Capacidad: 30 personas
Metros Cuadrados: 80.00
Piso: 3
Precio por Hora: $80.00
Equipamiento: Premium (Proyector HD, Pantalla gigante, Sistema de audio profesional, Micrófonos, Videoconferencia)
Foto: (opcional)
Estado: Activa
```

---

## 💼 ESCRITORIOS DEDICADOS (10 Escritorios)

### **Piso 1:**

#### Escritorio 1:
```
Código: ESC-101
Piso: 1
Posición: Junto a ventana norte
Tipo: Individual
Precio Mensual: $200.00
Estado: Disponible
Miembro Asignado: (ninguno)
```

#### Escritorio 2:
```
Código: ESC-102
Piso: 1
Posición: Centro sala
Tipo: Doble
Precio Mensual: $350.00
Estado: Ocupado
Miembro Asignado: Carlos Andrés Morales Vega
```

#### Escritorio 3:
```
Código: ESC-103
Piso: 1
Posición: Junto a ventana sur
Tipo: Individual
Precio Mensual: $200.00
Estado: Disponible
Miembro Asignado: (ninguno)
```

---

### **Piso 2:**

#### Escritorio 4:
```
Código: ESC-201
Piso: 2
Posición: Esquina noreste
Tipo: Triple
Precio Mensual: $500.00
Estado: Ocupado
Miembro Asignado: Ana Cristina Romero Flores
```

#### Escritorio 5:
```
Código: ESC-202
Piso: 2
Posición: Centro sala
Tipo: Individual
Precio Mensual: $220.00
Estado: Ocupado
Miembro Asignado: Valentina Alejandra Rojas Herrera
```

#### Escritorio 6:
```
Código: ESC-203
Piso: 2
Posición: Junto a ventana oeste
Tipo: Doble
Precio Mensual: $380.00
Estado: Disponible
Miembro Asignado: (ninguno)
```

---

### **Piso 3:**

#### Escritorio 7:
```
Código: ESC-301
Piso: 3
Posición: Vista panorámica norte
Tipo: Individual
Precio Mensual: $250.00
Estado: Ocupado
Miembro Asignado: Dr. Fernando José Ramírez Castillo
```

#### Escritorio 8:
```
Código: ESC-302
Piso: 3
Posición: Centro ejecutivo
Tipo: Triple
Precio Mensual: $550.00
Estado: Disponible
Miembro Asignado: (ninguno)
```

#### Escritorio 9:
```
Código: ESC-303
Piso: 3
Posición: Vista panorámica sur
Tipo: Doble
Precio Mensual: $400.00
Estado: Mantenimiento
Miembro Asignado: (ninguno)
```

#### Escritorio 10:
```
Código: ESC-304
Piso: 3
Posición: Esquina suroeste
Tipo: Individual
Precio Mensual: $240.00
Estado: Disponible
Miembro Asignado: (ninguno)
```

---

## 📅 RESERVAS DE EJEMPLO (5 Reservas)

### **Reserva 1:**
```
Miembro: Carlos Andrés Morales Vega (TechSolutions)
Sala: Sala Innovación
Fecha: [Hoy + 2 días]
Hora Inicio: 09:00
Hora Fin: 11:00
Número Asistentes: 6
Propósito: Reunión de planificación de proyecto nuevo
Costo Total: $60.00 (2 horas × $30)
Estado: Confirmada
```

---

### **Reserva 2:**
```
Miembro: Ana Cristina Romero Flores (Marketing Digital Pro)
Sala: Sala Colaborativa
Fecha: [Hoy + 3 días]
Hora Inicio: 14:00
Hora Fin: 16:00
Número Asistentes: 4
Propósito: Sesión de brainstorming con cliente
Costo Total: $50.00 (2 horas × $25)
Estado: Pendiente
```

---

### **Reserva 3:**
```
Miembro: Valentina Alejandra Rojas Herrera (Diseño Creativo)
Sala: Sala Meeting Point
Fecha: [Hoy + 1 día]
Hora Inicio: 10:00
Hora Fin: 12:00
Número Asistentes: 3
Propósito: Presentación de propuesta de diseño
Costo Total: $40.00 (2 horas × $20)
Estado: Confirmada
```

---

### **Reserva 4:**
```
Miembro: Dr. Fernando José Ramírez Castillo (LegalConsult)
Sala: Sala Ejecutiva
Fecha: [Hoy + 5 días]
Hora Inicio: 15:00
Hora Fin: 17:00
Número Asistentes: 10
Propósito: Junta directiva con clientes corporativos
Costo Total: $90.00 (2 horas × $45)
Estado: Confirmada
```

---

### **Reserva 5:**
```
Miembro: Roberto Carlos Gutiérrez Pérez (EcoVerde)
Sala: Sala Estrategia
Fecha: [Hoy + 4 días]
Hora Inicio: 11:00
Hora Fin: 13:00
Número Asistentes: 8
Propósito: Capacitación en normativas ambientales
Costo Total: $70.00 (2 horas × $35)
Estado: Pendiente
```

---

## 🎉 EVENTOS (4 Eventos)

### **Evento 1:**
```
Título: Networking Night: Conecta con Emprendedores
Descripción: Noche de networking para conocer a otros emprendedores del coworking, compartir experiencias y crear alianzas estratégicas. Incluye snacks y bebidas.
Organizador: TechSolutions Cía. Ltda.
Fecha: [Próximo viernes]
Hora Inicio: 18:00
Hora Fin: 21:00
Sala: Sala Auditorio
Capacidad Máxima: 30 personas
Tipo: Networking
Público: Sí
Foto: (opcional - imagen de networking)
```

---

### **Evento 2:**
```
Título: Workshop: Marketing Digital 2024
Descripción: Taller práctico sobre las últimas tendencias en marketing digital, redes sociales y SEO. Incluye certificado de participación.
Organizador: Marketing Digital Pro
Fecha: [Dentro de 10 días]
Hora Inicio: 09:00
Hora Fin: 13:00
Sala: Sala Ejecutiva
Capacidad Máxima: 12 personas
Tipo: Capacitación
Público: Sí
Foto: (opcional - imagen de workshop)
```

---

### **Evento 3:**
```
Título: Conferencia: Sostenibilidad Empresarial
Descripción: Conferencia sobre cómo implementar prácticas sostenibles en empresas, con casos de éxito reales. Expositor internacional.
Organizador: EcoVerde S.A.
Fecha: [Dentro de 15 días]
Hora Inicio: 16:00
Hora Fin: 18:00
Sala: Sala Auditorio
Capacidad Máxima: 30 personas
Tipo: Conferencia
Público: Sí
Foto: (opcional - imagen ecológica)
```

---

### **Evento 4:**
```
Título: Friday Social: Pizza & Cervezas
Descripción: Evento social para relajarse después de la semana de trabajo. Pizza, cervezas artesanales y música en vivo.
Organizador: Diseño Creativo Studio
Fecha: [Próximo viernes de la otra semana]
Hora Inicio: 19:00
Hora Fin: 22:00
Sala: (sin sala - área común)
Capacidad Máxima: 40 personas
Tipo: Social
Público: No (solo miembros)
Foto: (opcional - imagen festiva)
```

---

## 💰 FACTURAS (3 Facturas)

### **Factura 1:**
```
Número Factura: FACT-2024-001
Empresa: TechSolutions Cía. Ltda.
Fecha Emisión: 01/01/2024
Fecha Vencimiento: 15/01/2024
Detalles: Alquiler de escritorio ESC-102 (Doble) - Mes de Enero 2024
Subtotal: $350.00
IVA (15%): $52.50
Total: $402.50
Método de Pago: Transferencia
Estado: Pagada
```

---

### **Factura 2:**
```
Número Factura: FACT-2024-002
Empresa: Marketing Digital Pro
Fecha Emisión: 01/01/2024
Fecha Vencimiento: 15/01/2024
Detalles: Alquiler de escritorio ESC-201 (Triple) - Mes de Enero 2024
Subtotal: $500.00
IVA (15%): $75.00
Total: $575.00
Método de Pago: Tarjeta
Estado: Pagada
```

---

### **Factura 3:**
```
Número Factura: FACT-2024-003
Empresa: LegalConsult Abogados
Fecha Emisión: [Hoy]
Fecha Vencimiento: [Hoy + 15 días]
Detalles: Alquiler de escritorio ESC-301 (Individual) - Mes actual + Reservas de salas
Subtotal: $250.00
IVA (15%): $37.50
Total: $287.50
Método de Pago: Transferencia
Estado: Pendiente
```

---

## 📝 ORDEN DE INGRESO DE DATOS PARA PRUEBAS

### **Secuencia recomendada:**

1. ✅ **Iniciar servidor:**
```bash
cd c:\Django\django\CoworkSpaceKC
python manage.py runserver
```

2. ✅ **Crear superusuario** (si no existe):
```bash
python manage.py createsuperuser
```
Usuario: `admin`  
Email: `admin@coworkspace.ec`  
Password: `admin123` (cambiar en producción)

3. ✅ **Ingresar las 5 EMPRESAS** (en orden)

4. ✅ **Ingresar los 15 MIEMBROS** (3 por cada empresa)

5. ✅ **Ingresar las 6 SALAS DE REUNIÓN**

6. ✅ **Ingresar los 10 ESCRITORIOS**

7. ✅ **Asignar escritorios a miembros** (editar los que dicen "Ocupado")

8. ✅ **Crear las 5 RESERVAS** (usar el calendario)

9. ✅ **Crear los 4 EVENTOS**

10. ✅ **Generar las 3 FACTURAS**

11. ✅ **Ver REPORTES** y verificar estadísticas

---

## 🎯 CHECKLIST DE PRUEBAS

### **Módulo Empresas:**
- [ ] Crear 5 empresas
- [ ] Ver listado de empresas
- [ ] Editar una empresa
- [ ] Ver miembros de cada empresa
- [ ] Exportar tabla a Excel/PDF

### **Módulo Miembros:**
- [ ] Crear 3 miembros por empresa (15 total)
- [ ] Ver listado de miembros
- [ ] Editar un miembro
- [ ] Eliminar un miembro (prueba)

### **Módulo Salas:**
- [ ] Crear 6 salas
- [ ] Ver listado de salas
- [ ] Editar una sala
- [ ] Ver detalles con foto

### **Módulo Escritorios:**
- [ ] Crear 10 escritorios
- [ ] Ver listado de escritorios
- [ ] Asignar escritorios a miembros
- [ ] Ver mapa interactivo
- [ ] Arrastrar escritorios en el mapa

### **Módulo Reservas:**
- [ ] Crear 5 reservas
- [ ] Ver calendario de reservas
- [ ] Filtrar por sala
- [ ] Cambiar vista (mes/semana/día)
- [ ] Editar una reserva
- [ ] Cancelar una reserva

### **Módulo Eventos:**
- [ ] Crear 4 eventos
- [ ] Ver listado de eventos
- [ ] Ver detalles de evento
- [ ] Editar un evento

### **Módulo Facturas:**
- [ ] Generar 3 facturas
- [ ] Ver listado de facturas
- [ ] Marcar factura como pagada
- [ ] Exportar factura a PDF

### **Módulo Reportes:**
- [ ] Ver panel de reportes principal
- [ ] Ver reporte de ocupación (gráficos)
- [ ] Ver reporte de facturación (gráficos)
- [ ] Exportar reportes

---

## 💡 TIPS PARA PRUEBAS RÁPIDAS

1. **Usa Copy-Paste:** Copia los datos directamente de este manual
2. **Logos opcionales:** Puedes omitir las fotos/logos en las pruebas
3. **Fechas dinámicas:** Usa fechas futuras para reservas y eventos
4. **Prueba permisos:** Crea un usuario regular y verifica que solo ve sus datos
5. **Exporta datos:** Prueba exportar a Excel/PDF en todas las tablas
6. **Calendario:** Haz clic en diferentes vistas (mes, semana, día)
7. **Mapa interactivo:** Arrastra escritorios en el mapa
8. **Gráficos:** Verifica que los gráficos se generen correctamente

---

**¡Ahora tienes todos los datos para probar el sistema completo!** 🎉

**Tiempo estimado de ingreso:** 30-45 minutos  
**Empresas:** 5  
**Miembros:** 15  
**Salas:** 6  
**Escritorios:** 10  
**Reservas:** 5  
**Eventos:** 4  
**Facturas:** 3  

**Total:** ¡43 registros de prueba! 🚀
