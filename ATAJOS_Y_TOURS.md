# 🎯 Atajos de Teclado y Tours Guiados - CoworkSpace KC

## ⌨️ ATAJOS DE TECLADO PRINCIPALES

Todos los atajos usan la tecla **Alt** (no Ctrl) para evitar conflictos con el navegador.

### Atajos Globales (funcionan en toda la aplicación):
| Atajo | Acción | Descripción |
|-------|--------|-------------|
| `Alt+N` | Nueva Reserva | Abre el formulario para crear una nueva reserva de sala |
| `Alt+C` | Calendario | Va a la vista de calendario de reservas |
| `Alt+M` | Mapa | Abre el mapa interactivo de escritorios |

### Atajos Específicos:
| Atajo | Ubicación | Acción |
|-------|-----------|--------|
| `Alt+C` | Calendario | Va al día de hoy (Today) |

---

## 🎓 TOURS GUIADOS DISPONIBLES

Cada tour se muestra automáticamente la primera vez que visitas una sección. Usa Driver.js para guiar paso a paso.

### ✅ Tours Implementados:

1. **Tour de Inicio** 🏠
   - Ubicación: Página principal (`/`)
   - Contenido: Menú de navegación, accesos rápidos, atajos de teclado
   - Se activa: Primera vez que cargas la página de inicio

2. **Tour del Calendario** 📅
   - Ubicación: Calendario de reservas (`/reservas/calendario/`)
   - Contenido: Navegación del calendario, vistas, creación de reservas
   - Se activa: Primera vez que abres el calendario

3. **Tour del Mapa de Escritorios** 🗺️
   - Ubicación: Mapa interactivo (`/escritorios/mapa/`)
   - Contenido: Leyenda de colores, pisos, drag & drop (admin)
   - Se activa: Primera vez que abres el mapa

4. **Tour del Listado de Escritorios** 📋
   - Ubicación: Listado de escritorios (`/escritorios/`)
   - Contenido: Tabla DataTables, exportación, vista de mapa
   - Se activa: Primera vez que abres el listado

5. **Tour del Listado de Empresas** 🏢
   - Ubicación: Listado de empresas (`/empresas/`)
   - Contenido: Gestión de empresas, datos de contacto, miembros
   - Se activa: Primera vez que abres empresas

6. **Tour del Listado de Salas** 🚪
   - Ubicación: Listado de salas (`/salas/`)
   - Contenido: Información de salas, capacidad, equipamiento
   - Se activa: Primera vez que abres salas

7. **Tour del Listado de Eventos** ⭐
   - Ubicación: Listado de eventos (`/eventos/`)
   - Contenido: Eventos de networking, capacitaciones, conferencias
   - Se activa: Primera vez que abres eventos

8. **Tour de Nueva Factura** 💰
   - Ubicación: Formulario de factura (`/facturas/nuevo/`)
   - Contenido: Cálculo automático, IVA, exportación PDF
   - Se activa: Primera vez que creas una factura

---

## 🔄 REINICIAR TOURS

Si quieres ver los tours nuevamente, ejecuta esto en la consola del navegador (F12):

```javascript
// Reiniciar un tour específico:
localStorage.removeItem('tour_inicio_completado');
localStorage.removeItem('tour_calendario');
localStorage.removeItem('tour_mapa_escritorios');
localStorage.removeItem('tour_listado_escritorios');
localStorage.removeItem('tour_listado_empresas');
localStorage.removeItem('tour_listado_salas');
localStorage.removeItem('tour_listado_eventos');
localStorage.removeItem('tour_nueva_factura');

// O reiniciar TODOS los tours a la vez:
localStorage.clear();
```

Luego recarga la página (F5) y el tour volverá a aparecer.

---

## 📝 NOTAS IMPORTANTES

1. **Los atajos usan Alt+** en lugar de Ctrl+ para no interferir con atajos del navegador
   - Ctrl+R recarga la página (navegador)
   - Alt+R está libre para tu aplicación

2. **Tours no invasivos**: Solo aparecen la primera vez, luego se pueden reiniciar manualmente

3. **Compatibilidad**: Funciona en Chrome, Firefox, Edge y Safari

4. **Permisos**: Algunos tours muestran contenido diferente según si eres admin o usuario normal

---

## 🛠️ TECNOLOGÍAS USADAS

- **Hotkeys.js**: Para los atajos de teclado
- **Driver.js**: Para los tours guiados interactivos
- **localStorage**: Para recordar qué tours ya viste

---

**Última actualización**: 2026-07-29
**Versión**: 1.0
