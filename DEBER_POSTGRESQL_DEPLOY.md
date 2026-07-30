# 📚 DEBER: POSTGRESQL + DESPLIEGUE WEB

**Proyecto**: CoworkSpace KC  
**Fecha**: 29 de Julio, 2026  
**Objetivo**: Migrar a PostgreSQL y desplegar en Render.com

---

## 🎯 RESUMEN RÁPIDO (15 MINUTOS)

### ¿Qué hay que hacer?
1. **Migrar de SQLite a PostgreSQL** ✅ (Ya configurado)
2. **Desplegar en Render.com** (Más fácil y confiable)

### ¿Qué ya está listo?
- ✅ `settings.py` configurado para PostgreSQL
- ✅ `requirements.txt` con todas las dependencias
- ✅ `build.sh` que ejecuta migraciones y crea superusuario automáticamente
- ✅ `render.yaml` con configuración automática
- ✅ Código en GitHub: https://github.com/KellyDayana/CoworkSpaceKC

---

## ⚡ PASOS RÁPIDOS PARA RENDER

### PASO 1: Crear cuenta en Render (2 min)
1. Ve a: **https://render.com/**
2. Click en **"Get Started"** o **"Sign Up"**
3. Selecciona **"Sign up with GitHub"**
4. Autoriza a Render para acceder a tus repositorios

### PASO 2: Desplegar con Blueprint (5 min)
1. En Render dashboard, click en **"New +"** (arriba derecha)
2. Selecciona **"Blueprint"**
3. Busca y selecciona tu repositorio: **CoworkSpaceKC**
4. Render detectará automáticamente el archivo `render.yaml`
5. Dale un nombre al Blueprint: **coworkspace-kc**
6. Click en **"Apply"**

**¡Y eso es todo!** Render automáticamente:
- ✅ Creará una base de datos PostgreSQL
- ✅ Creará el servicio web
- ✅ Instalará dependencias
- ✅ Ejecutará migraciones
- ✅ Creará el superusuario (admin / admin123)
- ✅ Recopilará archivos estáticos

### PASO 3: Esperar el deploy (5 min)
1. Verás el progreso en tiempo real
2. Se mostrará el log del build:
   - "===== INSTALANDO DEPENDENCIAS ====="
   - "===== RECOPILANDO ARCHIVOS ESTÁTICOS ====="
   - "===== EJECUTANDO MIGRACIONES ====="
   - "===== CREANDO SUPERUSUARIO ====="
   - "===== BUILD COMPLETADO ====="
3. Cuando termine, verás: **"Live"** (en verde)

### PASO 4: Probar la aplicación (2 min)
1. Click en la URL que Render te da (algo como: `https://coworkspace-kc.onrender.com`)
2. Ve a: `https://tu-url.onrender.com/admin/`
3. Login con: **admin** / **admin123**
4. ¡Listo! 🎉

---

## 🆚 ¿POR QUÉ RENDER EN LUGAR DE RAILWAY?

| Característica | Render | Railway |
|----------------|--------|---------|
| **Facilidad** | ⭐⭐⭐⭐⭐ Muy fácil | ⭐⭐⭐ Medio |
| **PostgreSQL** | ✅ Incluido gratis | ✅ Incluido ($5/mes) |
| **Precio** | 🆓 100% gratis | 💵 $5 USD/mes gratis |
| **Build Scripts** | ✅ Ejecuta siempre | ⚠️ A veces falla |
| **Logs claros** | ✅ Muy claros | ⚠️ Confusos |
| **Django** | ✅ Optimizado | ⚠️ Requiere configuración |
| **Velocidad** | 🐌 30s para despertar | ⚡ Instantáneo |

**Desventaja de Render**: El plan gratuito "duerme" después de 15 minutos sin uso (tarda 30 segundos en despertar la primera vez).

**Ventaja de Render**: Es MÁS FÁCIL, más confiable, y perfecto para presentaciones de clase.

---

## 🐘 SOBRE POSTGRESQL

### ¿Qué cambió en el código?
**`settings.py`** ahora tiene:
```python
# Usa DATABASE_URL de Render automáticamente
try:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=f"postgresql://{os.environ.get('DB_USER', 'postgres')}:...",
            conn_max_age=600,
        )
    }
except ImportError:
    # Fallback a configuración manual
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.environ.get('DB_NAME', 'coworkspace_kc'),
            'USER': os.environ.get('DB_USER', 'postgres'),
            'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
            'HOST': os.environ.get('DB_HOST', 'localhost'),
            'PORT': os.environ.get('DB_PORT', '5432'),
        }
    }
```

### ¿Qué hace Render automáticamente?
- ✅ Crea la base de datos PostgreSQL
- ✅ Configura la variable `DATABASE_URL`
- ✅ Conecta Django con PostgreSQL
- ✅ Ejecuta `build.sh` automáticamente
- ✅ ¡Tú no haces nada!

---

## 📋 CHECKLIST PARA PRESENTACIÓN

### ANTES DE CLASE:
- [ ] Crear cuenta en Render: https://render.com/
- [ ] Deploy con Blueprint (seleccionar repositorio CoworkSpaceKC)
- [ ] Esperar a que termine el build (5-8 minutos)
- [ ] Verificar URL funciona: `https://coworkspace-kc.onrender.com/admin/`
- [ ] Login con: `admin` / `admin123`
- [ ] Cargar datos de prueba (empresas, salas, escritorios, reservas)

### EN CLASE (PRESENTACIÓN):
- [ ] Mostrar URL: `https://coworkspace-kc.onrender.com`
- [ ] Login al `/admin/`
- [ ] Crear empresa/sala/escritorio nuevo
- [ ] Recargar y mostrar que persiste (PostgreSQL funciona)
- [ ] Mostrar código en GitHub: https://github.com/KellyDayana/CoworkSpaceKC
- [ ] Mostrar panel Render con PostgreSQL conectado
- [ ] Mostrar logs del build mostrando migraciones

---

## 🎓 RESPUESTA A TU PREGUNTA DE ROLES

### Tu pregunta:
> "En el caso dice coordinador de carrera y el otro se definió como coordinador administrador de todo el sistema. ¿El coordinador de carrera sería solo en su carrera como un admin pero solo de la carrera, y el administrador sería de toda la facultad?"

### Respuesta: ¡SÍ, EXACTAMENTE!

**ARQUITECTURA CORRECTA**:

```
NIVEL 1: ADMINISTRADOR GENERAL (Superuser Django)
├─ Ve y gestiona TODAS las carreras
├─ Es el "Decano" o "Director de Facultad"
└─ Permisos globales en TODO el sistema

NIVEL 2: COORDINADOR DE CARRERA (Staff + Grupo "Coordinadores")
├─ Ve y gestiona SOLO SU CARRERA
├─ Es como un "admin local" limitado
├─ Ejemplo: Coordinador de Ing. Computación
└─ NO puede ver otras carreras

NIVEL 3: DOCENTE (Staff + Grupo "Docentes")
├─ Ve SOLO estudiantes de SUS materias
└─ Evalúa y gestiona SUS estudiantes

NIVEL 4: ESTUDIANTE (Usuario normal)
└─ Ve SOLO su propio perfil
```

### Implementación en Django:

```python
# models.py
class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    codigo = models.CharField(max_length=10)

class Coordinador(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)  # <-- CLAVE
    activo = models.BooleanField(default=True)

# views.py
@login_required
def lista_estudiantes(request):
    if request.user.is_superuser:
        # ADMIN: Ve TODOS los estudiantes de TODAS las carreras
        estudiantes = Estudiante.objects.all()
        
    elif request.user.groups.filter(name='Coordinadores').exists():
        # COORDINADOR: Ve SOLO estudiantes de SU carrera
        coordinador = Coordinador.objects.get(usuario=request.user)
        estudiantes = Estudiante.objects.filter(carrera=coordinador.carrera)
        
    elif request.user.groups.filter(name='Docentes').exists():
        # DOCENTE: Ve SOLO estudiantes de SUS materias
        docente = Docente.objects.get(usuario=request.user)
        estudiantes = Estudiante.objects.filter(
            materia__docente=docente
        ).distinct()
        
    else:
        # ESTUDIANTE: No ve listado
        estudiantes = Estudiante.objects.none()
    
    return render(request, 'estudiantes/lista.html', {
        'estudiantes': estudiantes
    })
```

**Diferencia clave**:
- **Administrador** = `is_superuser=True` → Ve TODO
- **Coordinador** = `staff=True` + `grupo="Coordinadores"` + `ForeignKey(Carrera)` → Ve SOLO su carrera

---

## 🆘 TROUBLESHOOTING

### Error: "no module named psycopg2"
```bash
pip install psycopg2-binary
```

### Error: "DisallowedHost"
En Render, esto no debería pasar porque `settings.py` usa `RENDER_EXTERNAL_HOSTNAME` automáticamente.

### Error: "500 Internal Server Error"
1. Ve a Render Dashboard → tu servicio
2. Click en "Logs" (panel izquierdo)
3. Busca el error específico
4. Normalmente es porque faltan migraciones: verifica que `build.sh` se ejecutó

### Sin estilos CSS
Render ejecuta `collectstatic` automáticamente en `build.sh`. Si no hay estilos:
1. Verifica los logs del build
2. Busca: "===== RECOPILANDO ARCHIVOS ESTÁTICOS ====="
3. Debería decir cuántos archivos copió

### No puedo hacer login con admin/admin123
1. Ve a Render → Logs
2. Busca: "===== CREANDO SUPERUSUARIO ====="
3. Debería decir: "Superusuario admin creado exitosamente"
4. Si dice que ya existe, las credenciales son correctas

### El sitio tarda mucho en cargar (primera vez)
Es normal en Render gratuito:
- El servicio "duerme" después de 15 minutos sin uso
- La primera petición tarda 30-50 segundos en despertar
- Después funciona normal
- **Tip para presentación**: Abre la URL 2 minutos antes de presentar

---

## 📞 COMANDOS ÚTILES (SI USAS CLI)

Render tiene CLI pero generalmente no lo necesitas. Todo se hace desde la web.

Si quieres instalarlo:
```bash
npm install -g @render/cli

# Login
render login

# Ver logs
render logs
```

---

## 📁 ARCHIVOS IMPORTANTES

### Creados para Render:
- ✅ `requirements.txt` - Dependencias Python
- ✅ `build.sh` - Script que ejecuta migraciones y setup
- ✅ `render.yaml` - Configuración automática (Blueprint)
- ✅ `.gitignore` - Archivos a ignorar en Git

### Modificados:
- ✅ `settings.py` - Configurado para PostgreSQL y Render
- ✅ `settings.py` - Variables de entorno
- ✅ `settings.py` - WhiteNoise para archivos estáticos
- ✅ `reservas/management/commands/crear_superusuario.py` - Comando personalizado

---

## ⏰ TIEMPO TOTAL: 15 MINUTOS

| Tarea | Tiempo |
|-------|--------|
| Crear cuenta en Render | 2 min |
| Deploy con Blueprint | 5 min |
| Esperar build | 5-8 min |
| Probar funcionamiento | 2 min |
| **TOTAL** | **15 min** |

---

## 🎉 PARA LA PRESENTACIÓN

**Prepara**:
- Link de tu app: `https://coworkspace-kc.onrender.com`
- Usuario admin: `admin` / `admin123`
- Repositorio: `https://github.com/KellyDayana/CoworkSpaceKC`

**Demuestra**:
1. App funcionando en vivo
2. Login al `/admin/`
3. Crear empresa/sala/escritorio nuevo
4. Recargar y mostrar que persiste (PostgreSQL funciona)
5. Mostrar código en GitHub
6. Mostrar panel Render con PostgreSQL conectado
7. Mostrar logs del build (migraciones, superusuario)

**Tip**: Abre la URL 2-3 minutos antes de presentar para que el servicio "despierte"

---

## 💡 NOTAS FINALES

- Render es **LA MEJOR OPCIÓN** para Django (más fácil que Railway)
- 100% GRATUITO (con limitación de "sleep" después de 15 min inactivos)
- PostgreSQL incluido automáticamente
- Build scripts funcionan perfectamente
- Los datos en PostgreSQL persisten entre deploys
- Render reinicia el servidor automáticamente en cada commit
- Perfecto para proyectos de clase y presentaciones

---

**¡Éxito en tu presentación!** 🚀

Si tienes problemas, lee la sección TROUBLESHOOTING arriba.
