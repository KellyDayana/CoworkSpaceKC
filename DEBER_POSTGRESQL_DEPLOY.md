# 📚 DEBER: POSTGRESQL + DESPLIEGUE WEB

**Proyecto**: CoworkSpace KC  
**Fecha**: 29 de Julio, 2026  
**Objetivo**: Migrar a PostgreSQL y desplegar en servidor web

---

## 🎯 RESUMEN RÁPIDO (25 MINUTOS)

### ¿Qué hay que hacer?
1. **Migrar de SQLite a PostgreSQL** ✅ (Ya configurado)
2. **Desplegar en servidor web** (Railway recomendado)

### ¿Qué ya está listo?
- ✅ `settings.py` configurado para PostgreSQL
- ✅ `requirements.txt` con todas las dependencias
- ✅ `Procfile` para gunicorn
- ✅ `runtime.txt` con Python 3.12
- ✅ `.env.example` con variables de entorno

---

## ⚡ PASOS RÁPIDOS

### PASO 1: Instalar dependencias (2 min)
```bash
cd c:\Django\django\CoworkSpaceKC
pip install -r requirements.txt
```

### PASO 2: Subir a GitHub (5 min)
```bash
# Crear .gitignore
echo *.pyc > .gitignore
echo __pycache__/ >> .gitignore
echo *.db >> .gitignore
echo *.sqlite3 >> .gitignore
echo .env >> .gitignore
echo staticfiles/ >> .gitignore
echo media/ >> .gitignore

# Inicializar Git
git init
git add .
git commit -m "Deploy con PostgreSQL"

# Crear repo en: https://github.com/new
# Nombre: CoworkSpaceKC

# Subir
git remote add origin https://github.com/TU_USUARIO/CoworkSpaceKC.git
git branch -M main
git push -u origin main
```

### PASO 3: Deploy en Railway (5 min)
1. Ve a: **https://railway.app/**
2. Login con GitHub
3. Click "New Project"
4. Selecciona "Deploy from GitHub repo"
5. Elige tu repositorio `CoworkSpaceKC`
6. Click "+ New" → "Database" → "Add PostgreSQL"
7. En "Variables", agrega:
   ```
   SECRET_KEY=django-insecure-8k#m+6@w^t9x$n2p-CAMBIA-ESTO-POR-ALGO-MUY-LARGO
   DEBUG=False
   ALLOWED_HOSTS=*.railway.app,*.up.railway.app
   ```

### PASO 4: Verificar que el deploy funcionó (2 min)

**¡IMPORTANTE!** No necesitas ejecutar comandos manualmente. El archivo `build.sh` ya hace todo automáticamente:
- ✅ Instala dependencias
- ✅ Ejecuta migraciones
- ✅ Crea superusuario (usuario: `admin`, contraseña: `admin123`)
- ✅ Recopila archivos estáticos

**Solo necesitas**:
1. Ve a tu proyecto en Railway
2. Click en "Deployments" (lado izquierdo)
3. Verifica que el último deploy diga "SUCCESS" ✅
4. Click en "View Logs" para ver que dice: `Superuser created` o `Superuser already exists`

**Si ves algún error en los logs**:
```bash
# Instalar Railway CLI (solo si hay problemas)
npm install -g @railway/cli

# Login
railway login

# Conectar al proyecto (selecciona "web", NO "Postgres")
railway link

# Ver logs en tiempo real
railway logs
```

### PASO 5: Probar la aplicación (2 min)
```bash
# Abrir en navegador
railway open

# O ve manualmente a tu URL en Railway
# https://web-production-XXXXX.up.railway.app
```

**Prueba lo siguiente**:
1. Abre tu URL de Railway
2. Deberías ver la página de login
3. Ve a: `https://tu-url.railway.app/admin/`
4. Login con: **usuario**: `admin`, **contraseña**: `admin123`
5. Si no puedes entrar, revisa los logs del deploy en Railway

---

## 🚂 ¿POR QUÉ RAILWAY?

- ✅ PostgreSQL incluido automáticamente
- ✅ Configuración automática de DATABASE_URL
- ✅ $5 USD gratis al mes (suficiente)
- ✅ Deploy en 5 minutos
- ✅ CLI para ejecutar comandos
- ✅ Logs en tiempo real

**Alternativa**: Render (100% gratis pero más lento)

---

## 🐘 SOBRE POSTGRESQL

### ¿Qué cambió en el código?
**`settings.py`** ahora tiene:
```python
# Prioriza DATABASE_URL (Railway), luego variables individuales
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

### ¿Qué hace Railway automáticamente?
- Crea la base de datos PostgreSQL
- Configura la variable `DATABASE_URL`
- Conecta Django con PostgreSQL
- ¡Tú no haces nada!

---

## 📋 CHECKLIST PARA MAÑANA

### HOY (hacer ahora):
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Subir a GitHub
- [ ] Deploy en Railway
- [ ] Verificar URL funciona: `railway open`

### MAÑANA (antes de clase):
- [ ] Abrir tu URL: `https://web-production-7b8ca.up.railway.app`
- [ ] Probar login en `/admin/` con: `admin` / `admin123`
- [ ] Cargar datos de prueba (empresas, salas, escritorios, reservas)
- [ ] Probar que PostgreSQL funciona (crear dato y recargar)
- [ ] Tomar captura del panel de Railway mostrando PostgreSQL

**Si el superusuario no funciona**:
1. Ve a Railway → tu proyecto → Deployments
2. Click en el último deploy
3. Click "View Logs"
4. Busca la línea que dice: `Superuser created` o `Superuser already exists`
5. Si dice "Superuser created", las credenciales son: `admin` / `admin123`

### EN CLASE (presentación):
- [ ] Mostrar URL: `https://tu-app.railway.app`
- [ ] Login al `/admin/`
- [ ] Crear un dato nuevo
- [ ] Recargar y mostrar que persiste (PostgreSQL)
- [ ] Mostrar código en GitHub
- [ ] Mostrar panel Railway con PostgreSQL

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

### ❌ Error: "Prohibido (403) - La verificación CSRF ha fallado"
**CAUSA**: Django en producción requiere configurar `CSRF_TRUSTED_ORIGINS`.

**SOLUCIÓN YA APLICADA**: 
- ✅ Agregado `CSRF_TRUSTED_ORIGINS` en `settings.py`
- ✅ Incluye: `https://*.railway.app` y `https://*.up.railway.app`
- ✅ Cambio ya está en GitHub y Railway lo desplegará automáticamente

**Si sigues viendo el error**:
1. Ve a Railway → tu proyecto → Deployments
2. Verifica que el último deploy diga "SUCCESS"
3. Espera 2-3 minutos después del deploy
4. Refresca tu navegador (Ctrl + F5 para limpiar caché)

### ❌ Error: UnicodeDecodeError al ejecutar `railway run`
**CAUSA**: La contraseña de PostgreSQL de Railway tiene caracteres especiales que Windows no procesa.

**SOLUCIÓN**: 
- ✅ **NO necesitas ejecutar `railway run` desde tu máquina local**
- ✅ El archivo `build.sh` ya ejecuta TODO automáticamente durante el deploy
- ✅ Solo verifica los logs en Railway para confirmar que se ejecutó correctamente

**Credenciales del superusuario creado automáticamente**:
- Usuario: `admin`
- Email: `admin@coworkspace.com`
- Contraseña: `admin123`

### Error: "no module named psycopg2"
```bash
pip install psycopg2-binary
```

### Error: "DisallowedHost"
- Ve a Railway → Variables
- Verifica que `ALLOWED_HOSTS=*.railway.app,*.up.railway.app`

### Error: "500 Internal Server Error"
```bash
# Ver logs
railway logs

# Probablemente necesitas migraciones
railway run python manage.py migrate
```

### Sin estilos CSS
```bash
# Esto se ejecuta automáticamente en build.sh
# Si aún no hay estilos, verifica que build.sh se ejecutó correctamente
railway logs
```

### No puedo crear superusuario manualmente
**NO LO NECESITAS**. El superusuario ya se creó automáticamente:
- Usuario: `admin`
- Contraseña: `admin123`

**Si olvidaste la contraseña**, puedes cambiarla desde Railway Shell:
```bash
railway link
railway shell
python manage.py changepassword admin
```

---

## 📞 COMANDOS ÚTILES

```bash
# Ver logs en tiempo real
railway logs

# Ejecutar cualquier comando Django
railway run python manage.py [comando]

# Abrir app en navegador
railway open

# Ver variables de entorno
railway variables

# Ver información del proyecto
railway status
```

---

## 📁 ARCHIVOS IMPORTANTES

### Ya creados por mí:
- ✅ `requirements.txt` - Dependencias
- ✅ `Procfile` - Comando de inicio
- ✅ `runtime.txt` - Versión Python
- ✅ `.env.example` - Template de variables
- ✅ `deploy_railway.bat` - Script automatizado (Windows)

### Modificados:
- ✅ `settings.py` - Configurado para PostgreSQL
- ✅ `settings.py` - Variables de entorno
- ✅ `settings.py` - WhiteNoise para archivos estáticos

---

## ⏰ TIEMPO TOTAL: 25 MINUTOS

| Tarea | Tiempo |
|-------|--------|
| Leer esta guía | 5 min |
| Instalar dependencias | 2 min |
| Subir a GitHub | 5 min |
| Deploy en Railway | 5 min |
| Ejecutar migraciones | 3 min |
| Crear superusuario | 2 min |
| Probar funcionamiento | 3 min |
| **TOTAL** | **25 min** |

---

## 🎉 PARA LA PRESENTACIÓN

**Prepara**:
- Link de tu app: `https://tu-app.railway.app`
- Usuario admin: `admin` / `contraseña`
- Repositorio: `https://github.com/tu-usuario/CoworkSpaceKC`

**Demuestra**:
1. App funcionando en vivo
2. Login al `/admin/`
3. Crear empresa/sala/escritorio nuevo
4. Recargar y mostrar que persiste (PostgreSQL funciona)
5. Mostrar código en GitHub
6. Mostrar panel Railway con PostgreSQL conectado

---

## 💡 NOTAS FINALES

- Railway es **LA OPCIÓN MÁS FÁCIL** porque incluye PostgreSQL automáticamente
- Render es alternativa 100% gratis pero más lenta
- PythonAnywhere **NO soporta PostgreSQL** en plan gratuito (NO usar)
- Railway te da $5 USD gratis (suficiente para todo el mes)
- Los datos en PostgreSQL persisten entre deploys
- Railway reinicia el servidor automáticamente en cada commit

---

**¡Éxito en tu presentación!** 🚀

Si tienes problemas, lee la sección TROUBLESHOOTING arriba.
