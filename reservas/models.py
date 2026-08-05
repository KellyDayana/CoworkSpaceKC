import os
from django.db import models
from django.contrib.auth.models import User


class EmpresaCliente(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    ruc = models.CharField(max_length=13, unique=True)  # RUC único
    telefono = models.CharField(max_length=15)
    email = models.EmailField(unique=True)  # Email único
    direccion = models.TextField()
    logo = models.FileField(upload_to='logos_empresas/', null=True, blank=True)
    fecha_registro = models.DateField(auto_now_add=True)
    
    PLAN_CHOICES = [
        ('basico', 'Básico'),
        ('profesional', 'Profesional'),
        ('empresarial', 'Empresarial'),
    ]
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='basico')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - {self.ruc}"


class Miembro(models.Model):
    id = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    empresa = models.ForeignKey(EmpresaCliente, on_delete=models.PROTECT, related_name='miembros')
    cedula = models.CharField(max_length=10, unique=True)  # UNIQUE: No permite cédulas duplicadas
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Email único
    telefono = models.CharField(max_length=15)
    foto = models.FileField(upload_to='fotos_miembros/', null=True, blank=True)
    
    CARGO_CHOICES = [
        ('gerente', 'Gerente'),
        ('empleado', 'Empleado'),
        ('freelancer', 'Freelancer'),
    ]
    cargo = models.CharField(max_length=20, choices=CARGO_CHOICES, default='empleado')
    fecha_ingreso = models.DateField()
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.empresa.nombre}"


class SalaReunion(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    capacidad = models.PositiveIntegerField()
    metros_cuadrados = models.DecimalField(max_digits=6, decimal_places=2)
    piso = models.PositiveIntegerField()
    foto = models.FileField(upload_to='salas/', null=True, blank=True)
    precio_hora = models.DecimalField(max_digits=8, decimal_places=2)
    
    EQUIPAMIENTO_CHOICES = [
        ('basico', 'Básico (Mesa y Sillas)'),
        ('ejecutivo', 'Ejecutivo (+ Proyector)'),
        ('premium', 'Premium (+ TV, Videoconferencia)'),
    ]
    equipamiento = models.CharField(max_length=20, choices=EQUIPAMIENTO_CHOICES, default='basico')
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} - Capacidad: {self.capacidad} personas"


class EscritorioDedicado(models.Model):
    id = models.AutoField(primary_key=True)
    codigo = models.CharField(max_length=20, unique=True)
    piso = models.PositiveIntegerField()
    posicion = models.PositiveIntegerField(default=1)  # Posición horizontal 1-10
    precio_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    
    TIPO_CHOICES = [
        ('individual', 'Individual'),
        ('compartido', 'Compartido'),
        ('privado', 'Privado'),
    ]
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='individual')
    
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('ocupado', 'Ocupado'),
        ('mantenimiento', 'Mantenimiento'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    miembro_asignado = models.ForeignKey(Miembro, on_delete=models.SET_NULL, null=True, blank=True, related_name='escritorios')

    class Meta:
        # Solo una posición por piso (horizontal 1-10)
        unique_together = ['piso', 'posicion']
        ordering = ['piso', 'posicion']

    def __str__(self):
        return f"Escritorio {self.codigo} - Piso {self.piso} - Posición {self.posicion} - {self.estado}"


class ReservaSala(models.Model):
    id = models.AutoField(primary_key=True)
    sala = models.ForeignKey(SalaReunion, on_delete=models.PROTECT, related_name='reservas')  # PROTECT: No permitir eliminar sala con reservas
    miembro = models.ForeignKey(Miembro, on_delete=models.PROTECT, related_name='reservas_salas')  # PROTECT: No permitir eliminar miembro con reservas
    fecha = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    proposito = models.CharField(max_length=200)
    numero_asistentes = models.PositiveIntegerField()
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('confirmada', 'Confirmada'),
        ('completada', 'Completada'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='confirmada')
    costo_total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sala.nombre} - {self.fecha} {self.hora_inicio} - {self.miembro.nombre}"


class Evento(models.Model):
    id = models.AutoField(primary_key=True)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    organizador = models.ForeignKey(EmpresaCliente, on_delete=models.PROTECT, related_name='eventos')  # PROTECT: No eliminar empresa con eventos
    fecha_evento = models.DateField()
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    sala = models.ForeignKey(SalaReunion, on_delete=models.SET_NULL, related_name='eventos', null=True, blank=True)  # SET_NULL: Si se elimina sala, evento sin sala
    capacidad_maxima = models.PositiveIntegerField()
    foto = models.FileField(upload_to='eventos/', null=True, blank=True)
    
    TIPO_CHOICES = [
        ('networking', 'Networking'),
        ('capacitacion', 'Capacitación'),
        ('conferencia', 'Conferencia'),
        ('social', 'Social'),
    ]
    tipo_evento = models.CharField(max_length=20, choices=TIPO_CHOICES, default='networking')
    publico = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titulo} - {self.fecha_evento}"


class Factura(models.Model):
    id = models.AutoField(primary_key=True)
    empresa = models.ForeignKey(EmpresaCliente, on_delete=models.PROTECT, related_name='facturas')  # PROTECT: No eliminar empresa con facturas
    numero_factura = models.CharField(max_length=20, unique=True)
    fecha_emision = models.DateField(auto_now_add=True)
    fecha_vencimiento = models.DateField()
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    iva = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    pdf = models.FileField(upload_to='facturas/', null=True, blank=True)
    
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
        ('cancelada', 'Cancelada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='pendiente')
    
    TIPO_CHOICES = [
        ('mensual', 'Mensualidad'),
        ('reservas', 'Reservas de Salas'),
        ('evento', 'Evento'),
        ('otros', 'Otros Servicios'),
    ]
    tipo_factura = models.CharField(max_length=20, choices=TIPO_CHOICES, default='mensual')
    
    notas = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.numero_factura:
            last_factura = Factura.objects.order_by('-id').first()
            if last_factura and last_factura.numero_factura:
                try:
                    last_num = int(last_factura.numero_factura.split('-')[1])
                    self.numero_factura = f'FAC-{str(last_num + 1).zfill(6)}'
                except:
                    self.numero_factura = 'FAC-000001'
            else:
                self.numero_factura = 'FAC-000001'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_factura} - {self.empresa.nombre} - ${self.total}"
