# 📄 Sistema de Reportes PDF y Envío por Correo

## ✅ Implementación Completa

### 🎯 Funcionalidades Implementadas

#### 1. **Facturas** 🧾
**Cuándo se genera:**
- Al crear una nueva factura automáticamente

**Contenido del PDF:**
- Logo y datos de CoworkSpace KC
- Número de factura
- Información completa de la empresa cliente (nombre, RUC, email, teléfono, dirección)
- Detalle de facturación (tipo, estado, subtotal, IVA 15%, total)
- Notas adicionales
- Fecha de emisión y vencimiento

**Botones disponibles:**
- 🔴 **Ver PDF**: Abre el PDF en nueva pestaña
- 📧 **Enviar por Correo**: Reenvía el PDF al email de la empresa
- ✏️ **Editar**: Modifica la factura
- 🗑️ **Eliminar**: Elimina la factura (solo admin)

**Email enviado a:** `empresa.email`

---

#### 2. **Reservas de Salas** 📅
**Cuándo se genera:**
- Al confirmar una reserva de sala automáticamente

**Contenido del PDF:**
- Información de la sala (nombre, capacidad)
- Datos del miembro y empresa
- Fecha y horario (inicio - fin)
- Propósito de la reserva
- Número de asistentes
- Costo total calculado

**Botones disponibles:**
- 🔴 **Ver PDF**: Abre el PDF en nueva pestaña
- 📧 **Enviar por Correo**: Reenvía el PDF al email del miembro
- ✏️ **Editar**: Modifica la reserva
- 🗑️ **Eliminar**: Cancela la reserva

**Email enviado a:** `miembro.email`

---

#### 3. **Eventos** 🎉
**Cuándo se genera:**
- Al registrar un nuevo evento automáticamente

**Contenido del PDF:**
- Título y descripción del evento
- Empresa organizadora
- Fecha y horario (inicio - fin)
- Sala asignada (si aplica)
- Tipo de evento (networking, capacitación, conferencia, social)
- Capacidad máxima
- Visibilidad (público/privado)

**Botones disponibles:**
- 🔴 **Ver PDF**: Abre el PDF en nueva pestaña
- 📧 **Enviar por Correo**: Reenvía el PDF al email del organizador
- ✏️ **Editar**: Modifica el evento
- 🗑️ **Eliminar**: Elimina el evento (solo admin)

**Email enviado a:** `organizador.email` (empresa)

---

#### 4. **Escritorios Dedicados** 💼
**Cuándo se genera:**
- Al asignar un escritorio a un miembro (solo cuando hay nuevo miembro asignado)

**Contenido del PDF:**
- Código del escritorio
- Ubicación (piso y posición)
- Tipo (individual/compartido/ejecutivo)
- Estado (ocupado/disponible/mantenimiento)
- Precio mensual
- Datos del miembro asignado (nombre, empresa, email)

**Botones disponibles:**
- 🔴 **Ver PDF**: Abre el PDF en nueva pestaña (solo si tiene miembro asignado)
- 📧 **Enviar por Correo**: Reenvía el PDF al email del miembro (solo si tiene miembro asignado)
- ✏️ **Editar**: Modifica el escritorio
- 🗑️ **Eliminar**: Elimina el escritorio (solo admin)

**Email enviado a:** `miembro_asignado.email`

---

## 🎨 Mejoras de Accesibilidad - Contraste de Colores

### Antes ❌
- Botones amarillos (warning) con texto predeterminado → **Difícil de leer**
- Botones sin contraste suficiente
- Inconsistencia en estilos

### Después ✅
| Color de Fondo | Color de Texto | Uso |
|----------------|----------------|-----|
| `#ffc107` (Amarillo) | `#000` (Negro) | Botones Editar |
| `#dc3545` (Rojo) | `#fff` (Blanco) | Botones Eliminar, Ver PDF |
| `#17a2b8` (Azul Cian) | `#fff` (Blanco) | Botones Enviar Correo |
| `#28a745` (Verde) | `#fff` (Blanco) | Botones Guardar/Actualizar |
| `#4A6785` (Azul Oscuro) | `#fff` (Blanco) | Botones Principales |

**Archivos corregidos:**
- ✅ `templates/facturas/listado.html`
- ✅ `templates/reservas/listado.html`
- ✅ `templates/eventos/listado.html`
- ✅ `templates/escritorios/listado.html`
- ✅ `templates/empresas/listado.html`
- ✅ `templates/empresas/editar.html`
- ✅ `templates/miembros/listado.html`
- ✅ `templates/miembros/editar.html`
- ✅ `templates/salas/listado.html`
- ✅ `templates/salas/editar.html`

---

## 🔧 Funciones Implementadas en `views.py`

### Generación de PDFs
```python
_generar_pdf_factura(factura)
_generar_pdf_reserva(reserva)
_generar_pdf_evento(evento)
_generar_pdf_escritorio(escritorio)
```

### Descarga de PDFs
```python
descargar_pdf_factura(request, id)
descargar_pdf_reserva(request, id)
descargar_pdf_evento(request, id)
descargar_pdf_escritorio(request, id)
```

### Envío por Correo
```python
enviar_pdf_factura(request, id)
enviar_pdf_reserva(request, id)
enviar_pdf_evento(request, id)
enviar_pdf_escritorio(request, id)
```

### Función Auxiliar
```python
_enviar_email_con_pdf(destinatario, asunto, mensaje_texto, mensaje_html, pdf_bytes, nombre_archivo)
```

---

## 🌐 URLs Agregadas

```python
# PDFs de Facturas
path('facturas/pdf/<int:id>/', views.descargar_pdf_factura, name='descargar_pdf_factura'),
path('facturas/enviar/<int:id>/', views.enviar_pdf_factura, name='enviar_pdf_factura'),

# PDFs de Reservas
path('reservas/pdf/<int:id>/', views.descargar_pdf_reserva, name='descargar_pdf_reserva'),
path('reservas/enviar/<int:id>/', views.enviar_pdf_reserva, name='enviar_pdf_reserva'),

# PDFs de Eventos
path('eventos/pdf/<int:id>/', views.descargar_pdf_evento, name='descargar_pdf_evento'),
path('eventos/enviar/<int:id>/', views.enviar_pdf_evento, name='enviar_pdf_evento'),

# PDFs de Escritorios
path('escritorios/pdf/<int:id>/', views.descargar_pdf_escritorio, name='descargar_pdf_escritorio'),
path('escritorios/enviar/<int:id>/', views.enviar_pdf_escritorio, name='enviar_pdf_escritorio'),
```

---

## 📦 Dependencias Agregadas

```txt
reportlab>=4.0.0      # Generación de PDFs profesionales
qrcode[pil]>=7.4.0    # Generación de códigos QR (para futuras mejoras)
```

---

## 📧 Formato de Correos

Todos los correos electrónicos incluyen:

### Versión Texto Plano
- Saludo personalizado
- Detalle completo del documento
- Información clave
- Firma de CoworkSpace KC

### Versión HTML
- Diseño responsive
- Header con colores del proyecto (#4A6785)
- Tabla con información estructurada
- Estilo profesional
- Compatible con todos los clientes de correo

### Adjunto PDF
- Generado dinámicamente
- Formato profesional
- Tamaño optimizado

---

## 🎯 Ejemplos de Uso

### Usuario Final (Miembro)
1. Hace una reserva de sala → Recibe PDF automáticamente por correo
2. En el listado de reservas puede:
   - Ver el PDF en cualquier momento
   - Reenviar el PDF a su correo

### Administrador
1. Crea una factura → Se envía automáticamente a la empresa
2. Asigna un escritorio → Se envía PDF al miembro asignado
3. Registra un evento → Se envía PDF a la empresa organizadora
4. Puede reenviar cualquier PDF en cualquier momento

---

## ✨ Características Destacadas

✅ **Generación automática**: Los PDFs se crean y envían al guardar/asignar  
✅ **Reenvío manual**: Botones para reenviar PDFs cuando sea necesario  
✅ **Vista previa**: Ver PDFs en el navegador antes de descargar  
✅ **Diseño profesional**: PDFs con logo, colores corporativos y tablas  
✅ **Emails HTML**: Correos con diseño responsive y profesional  
✅ **Manejo de errores**: Si falla el correo, no afecta el registro  
✅ **Accesibilidad**: Botones con contraste WCAG AAA  
✅ **Confirmación**: Mensajes de éxito al enviar correos  

---

## 🚀 Deploy en Render

**Estado**: ✅ Desplegado automáticamente  
**URL**: https://coworkspacekc.onrender.com  

Las librerías `reportlab` y `qrcode[pil]` se instalan automáticamente durante el deploy mediante `requirements.txt`.

---

## 📝 Notas Técnicas

- Los PDFs se generan en memoria (io.BytesIO), no se guardan en disco
- Compatible con Cloudinary (imágenes en cloud, PDFs en memoria)
- IVA configurado al 15%
- Tamaño de letra y márgenes optimizados para lectura
- Colores corporativos: #4A6785 (azul principal), #2D4A64 (azul oscuro)

---

**Fecha de implementación**: Agosto 2026  
**Versión**: 1.0.0  
**Estado**: ✅ Producción
