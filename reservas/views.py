import os
import json
from datetime import datetime, date
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse, HttpResponse
from django.core.mail import send_mail, EmailMultiAlternatives
from django.conf import settings
import io

# Importar ReportLab para PDFs
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT

from .models import (
    EmpresaCliente, Miembro, SalaReunion, EscritorioDedicado,
    ReservaSala, Evento, Factura
)


# ==================== FUNCIONES DE GENERACIÓN DE PDFs ====================

def _generar_pdf_factura(factura):
    """Genera PDF de factura y devuelve los bytes"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'TituloFactura', parent=styles['Title'], textColor=colors.HexColor('#4A6785'),
        fontSize=22, alignment=TA_CENTER, spaceAfter=2,
    )
    subtitulo_style = ParagraphStyle(
        'Subtitulo', parent=styles['Normal'], textColor=colors.HexColor('#555555'),
        fontSize=10, alignment=TA_CENTER, spaceAfter=14,
    )
    
    story = []
    story.append(Paragraph('CoworkSpace KC', titulo_style))
    story.append(Paragraph('Plataforma de Reservas para Edificios de Coworking - FACTURA', subtitulo_style))
    story.append(Paragraph(f'Factura N°: {factura.numero_factura}', ParagraphStyle(
        'Numero', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=13, 
        textColor=colors.HexColor('#4A6785'), fontName='Helvetica-Bold', spaceAfter=4
    )))
    story.append(Paragraph(
        f'Fecha: {factura.fecha_emision.strftime("%d/%m/%Y")}',
        ParagraphStyle('Fecha', parent=styles['Normal'], alignment=TA_RIGHT, fontSize=9, textColor=colors.grey)
    ))
    
    # Datos de la empresa
    story.append(Spacer(1, 10))
    story.append(Paragraph('Empresa Cliente', ParagraphStyle(
        'Seccion', parent=styles['Heading2'], textColor=colors.HexColor('#1F1F1F'),
        fontSize=12, spaceBefore=14, spaceAfter=6,
    )))
    datos_empresa = [
        ['Empresa:', factura.empresa.nombre],
        ['RUC:', factura.empresa.ruc],
        ['Email:', factura.empresa.email],
        ['Teléfono:', factura.empresa.telefono],
        ['Dirección:', factura.empresa.direccion],
    ]
    tabla_empresa = Table(datos_empresa, colWidths=[35 * mm, 130 * mm])
    tabla_empresa.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(tabla_empresa)
    
    # Detalle de la factura
    story.append(Spacer(1, 10))
    story.append(Paragraph('Detalle de Facturación', ParagraphStyle(
        'Seccion', parent=styles['Heading2'], textColor=colors.HexColor('#1F1F1F'),
        fontSize=12, spaceBefore=14, spaceAfter=6,
    )))
    datos_factura = [
        ['Tipo:', factura.get_tipo_factura_display()],
        ['Estado:', factura.get_estado_display()],
        ['Subtotal:', f'${factura.subtotal}'],
        ['IVA (15%):', f'${factura.iva}'],
        ['Notas:', factura.notas or 'N/A'],
    ]
    tabla_factura = Table(datos_factura, colWidths=[35 * mm, 130 * mm])
    tabla_factura.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9.5),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tabla_factura)
    
    # Total
    story.append(Spacer(1, 14))
    tabla_total = Table([['TOTAL', f'${factura.total}']], colWidths=[135 * mm, 30 * mm])
    tabla_total.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#4A6785')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('ALIGN', (1, 0), (1, 0), 'RIGHT'),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
    ]))
    story.append(tabla_total)
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        'CoworkSpace KC &middot; info@coworkspacekc.com',
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _generar_pdf_reserva(reserva):
    """Genera PDF de confirmación de reserva de sala y devuelve los bytes"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Title'], textColor=colors.HexColor('#4A6785'),
        fontSize=22, alignment=TA_CENTER, spaceAfter=2,
    )
    
    story = []
    story.append(Paragraph('CoworkSpace KC', titulo_style))
    story.append(Paragraph('CONFIRMACIÓN DE RESERVA DE SALA', ParagraphStyle(
        'Subtitulo', parent=styles['Normal'], textColor=colors.HexColor('#555555'),
        fontSize=10, alignment=TA_CENTER, spaceAfter=14,
    )))
    
    # Datos de la reserva
    datos = [
        ['Sala:', reserva.sala.nombre],
        ['Miembro:', f'{reserva.miembro.nombre} {reserva.miembro.apellido}'],
        ['Empresa:', reserva.miembro.empresa.nombre],
        ['Fecha:', reserva.fecha.strftime('%d/%m/%Y')],
        ['Hora Inicio:', reserva.hora_inicio.strftime('%H:%M')],
        ['Hora Fin:', reserva.hora_fin.strftime('%H:%M')],
        ['Propósito:', reserva.proposito],
        ['Asistentes:', str(reserva.numero_asistentes)],
        ['Estado:', reserva.get_estado_display()],
        ['Costo Total:', f'${reserva.costo_total}'],
    ]
    tabla = Table(datos, colWidths=[40 * mm, 125 * mm])
    tabla.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tabla)
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        'Gracias por usar CoworkSpace KC',
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _generar_pdf_evento(evento):
    """Genera PDF de confirmación de evento y devuelve los bytes"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Title'], textColor=colors.HexColor('#4A6785'),
        fontSize=22, alignment=TA_CENTER, spaceAfter=2,
    )
    
    story = []
    story.append(Paragraph('CoworkSpace KC', titulo_style))
    story.append(Paragraph('CONFIRMACIÓN DE EVENTO', ParagraphStyle(
        'Subtitulo', parent=styles['Normal'], textColor=colors.HexColor('#555555'),
        fontSize=10, alignment=TA_CENTER, spaceAfter=14,
    )))
    
    # Datos del evento
    datos = [
        ['Título:', evento.titulo],
        ['Descripción:', evento.descripcion],
        ['Organizador:', evento.organizador.nombre],
        ['Fecha:', evento.fecha_evento.strftime('%d/%m/%Y')],
        ['Hora Inicio:', evento.hora_inicio.strftime('%H:%M')],
        ['Hora Fin:', evento.hora_fin.strftime('%H:%M')],
        ['Sala:', evento.sala.nombre if evento.sala else 'Sin sala asignada'],
        ['Tipo:', evento.get_tipo_evento_display()],
        ['Capacidad Máxima:', str(evento.capacidad_maxima)],
        ['Público:', 'Sí' if evento.publico else 'No'],
    ]
    tabla = Table(datos, colWidths=[40 * mm, 125 * mm])
    tabla.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(tabla)
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        'Gracias por usar CoworkSpace KC',
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _generar_pdf_escritorio(escritorio):
    """Genera PDF de asignación de escritorio y devuelve los bytes"""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=letter,
        topMargin=20 * mm, bottomMargin=20 * mm,
        leftMargin=20 * mm, rightMargin=20 * mm,
    )
    styles = getSampleStyleSheet()
    titulo_style = ParagraphStyle(
        'Titulo', parent=styles['Title'], textColor=colors.HexColor('#4A6785'),
        fontSize=22, alignment=TA_CENTER, spaceAfter=2,
    )
    
    story = []
    story.append(Paragraph('CoworkSpace KC', titulo_style))
    story.append(Paragraph('ASIGNACIÓN DE ESCRITORIO DEDICADO', ParagraphStyle(
        'Subtitulo', parent=styles['Normal'], textColor=colors.HexColor('#555555'),
        fontSize=10, alignment=TA_CENTER, spaceAfter=14,
    )))
    
    # Datos del escritorio
    datos = [
        ['Código:', escritorio.codigo],
        ['Piso:', str(escritorio.piso)],
        ['Posición:', str(escritorio.posicion)],
        ['Tipo:', escritorio.get_tipo_display()],
        ['Estado:', escritorio.get_estado_display()],
        ['Precio Mensual:', f'${escritorio.precio_mensual}'],
    ]
    
    if escritorio.miembro_asignado:
        datos.extend([
            ['Miembro Asignado:', f'{escritorio.miembro_asignado.nombre} {escritorio.miembro_asignado.apellido}'],
            ['Empresa:', escritorio.miembro_asignado.empresa.nombre],
            ['Email:', escritorio.miembro_asignado.email],
        ])
    
    tabla = Table(datos, colWidths=[45 * mm, 120 * mm])
    tabla.setStyle(TableStyle([
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#888888')),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(tabla)
    
    story.append(Spacer(1, 30))
    story.append(Paragraph(
        'Gracias por usar CoworkSpace KC',
        ParagraphStyle('Footer', parent=styles['Normal'], alignment=TA_CENTER, fontSize=8, textColor=colors.grey)
    ))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()


def _enviar_email_con_pdf(destinatario, asunto, mensaje_texto, mensaje_html, pdf_bytes, nombre_archivo):
    """Función genérica para enviar email con PDF adjunto"""
    try:
        email = EmailMultiAlternatives(
            subject=asunto,
            body=mensaje_texto,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[destinatario]
        )
        email.attach_alternative(mensaje_html, 'text/html')
        email.attach(nombre_archivo, pdf_bytes, 'application/pdf')
        email.send(fail_silently=True)
        return True
    except Exception as e:
        print(f'Error enviando email: {e}')
        return False


# ==================== AUTENTICACIÓN ====================

def login_view(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            login(request, user)
            return redirect('inicio')
        else:
            messages.error(request, 'Credenciales inválidas.')
    return render(request, 'auth/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')


def registro_view(request):
    # Obtener empresas activas para el selector
    empresas = EmpresaCliente.objects.filter(activo=True)
    
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        clave_confirm = request.POST.get('password_confirm')
        empresa_id = request.POST.get('empresa')
        
        # Datos del miembro
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        cargo = request.POST.get('cargo', 'empleado')
        
        if clave != clave_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return render(request, 'auth/registro.html', {'empresas': empresas})
        
        if User.objects.filter(username=usuario).exists():
            messages.error(request, 'El usuario ya existe.')
            return render(request, 'auth/registro.html', {'empresas': empresas})
        
        if User.objects.filter(email=correo).exists():
            messages.error(request, 'El email ya está registrado.')
            return render(request, 'auth/registro.html', {'empresas': empresas})
        
        if not empresa_id:
            messages.error(request, 'Debes seleccionar una empresa.')
            return render(request, 'auth/registro.html', {'empresas': empresas})
        
        # Crear usuario
        user = User.objects.create_user(username=usuario, email=correo, password=clave)
        
        # Crear miembro asociado a la empresa
        empresa = get_object_or_404(EmpresaCliente, id=empresa_id)
        miembro = Miembro.objects.create(
            usuario=user,
            empresa=empresa,
            cedula=cedula,
            nombre=nombre,
            apellido=apellido,
            email=correo,
            telefono=telefono,
            cargo=cargo,
            fecha_ingreso=date.today(),
            activo=True
        )
        
        # Enviar email de bienvenida
        try:
            asunto = '¡Bienvenido a CoworkSpace KC!'
            mensaje = f'''
Hola {nombre} {apellido},

¡Bienvenido a CoworkSpace KC!

Tu cuenta ha sido creada exitosamente con los siguientes datos:

👤 Usuario: {usuario}
📧 Email: {correo}
🏢 Empresa: {empresa.nombre}
💼 Cargo: {dict(Miembro.CARGO_CHOICES).get(cargo, cargo)}

Ya puedes iniciar sesión y explorar nuestros espacios de coworking.

Saludos,
Equipo CoworkSpace KC
            '''
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [correo],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error enviando email: {e}")
        
        # Iniciar sesión automáticamente
        login(request, user)
        messages.success(request, f'¡Bienvenido {nombre}! Tu cuenta ha sido creada exitosamente en {empresa.nombre}.')
        return redirect('inicio')
    
    return render(request, 'auth/registro.html', {'empresas': empresas})


# ==================== INICIO Y DASHBOARD ====================

def inicio(request):
    # Vista pública del inicio (no requiere login)
    # Estadísticas básicas para mostrar
    total_empresas = EmpresaCliente.objects.filter(activo=True).count()
    total_salas = SalaReunion.objects.filter(activo=True).count()
    total_eventos = Evento.objects.filter(publico=True).count()
    
    context = {
        'total_empresas': total_empresas,
        'total_salas': total_salas,
        'total_eventos': total_eventos,
    }
    return render(request, 'base/inicio.html', context)


@login_required
@login_required
def dashboard(request):
    # Solo administradores pueden acceder al dashboard global
    if not request.user.is_superuser:
        messages.warning(request, 'El Dashboard solo está disponible para administradores.')
        return redirect('inicio')
    
    # Dashboard con métricas detalladas
    empresas = EmpresaCliente.objects.filter(activo=True)
    salas = SalaReunion.objects.filter(activo=True)
    escritorios = EscritorioDedicado.objects.all()
    
    # Calcular tasa de ocupación de escritorios
    total_escritorios = escritorios.count()
    escritorios_ocupados = escritorios.filter(estado='ocupado').count()
    tasa_ocupacion = (escritorios_ocupados / total_escritorios * 100) if total_escritorios > 0 else 0
    
    # Calcular metros cuadrados ocupados
    total_metros = sum([sala.metros_cuadrados for sala in salas])
    
    context = {
        'empresas': empresas,
        'tasa_ocupacion': round(tasa_ocupacion, 2),
        'total_metros': total_metros,
        'escritorios_ocupados': escritorios_ocupados,
        'total_escritorios': total_escritorios,
    }
    return render(request, 'base/dashboard.html', context)


# ==================== CRUD EMPRESAS CLIENTES ====================

@login_required
def empresa_lista(request):
    if request.user.is_superuser:
        # Administrador ve todas las empresas
        empresas = EmpresaCliente.objects.all()
    else:
        # Usuario normal ve solo su empresa (si tiene miembro asociado)
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            empresas = EmpresaCliente.objects.filter(id=miembro.empresa.id)
        except Miembro.DoesNotExist:
            # Si no tiene miembro asociado, no ve ninguna empresa
            empresas = EmpresaCliente.objects.none()
            messages.warning(request, 'No tienes una empresa asociada. Contacta al administrador.')
    return render(request, 'empresas/listado.html', {'empresas': empresas})


@login_required
def nueva_empresa(request):
    # Solo administradores pueden crear empresas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear empresas.')
        return redirect('empresa_lista')
    return render(request, 'empresas/nuevo.html')


@login_required
def guardar_empresa(request):
    # Solo administradores pueden crear empresas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear empresas.')
        return redirect('empresa_lista')
    
    if request.method == 'POST':
        EmpresaCliente.objects.create(
            nombre=request.POST['nombre'],
            ruc=request.POST['ruc'],
            telefono=request.POST['telefono'],
            email=request.POST['email'],
            direccion=request.POST['direccion'],
            plan=request.POST['plan'],
            logo=request.FILES.get('logo'),
            activo='activo' in request.POST
        )
        messages.success(request, 'Empresa guardada correctamente.')
        return redirect('empresa_lista')


@login_required
def editar_empresa(request, id):
    empresa = get_object_or_404(EmpresaCliente, id=id)
    
    # Verificar permisos: admin puede editar todas, usuario normal solo su empresa
    if not request.user.is_superuser:
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            if miembro.empresa.id != empresa.id:
                messages.error(request, 'No tienes permisos para editar esta empresa.')
                return redirect('empresa_lista')
        except Miembro.DoesNotExist:
            messages.error(request, 'No tienes permisos para editar empresas.')
            return redirect('empresa_lista')
    
    return render(request, 'empresas/editar.html', {'empresa': empresa})


@login_required
def procesar_edicion_empresa(request):
    if request.method == 'POST':
        empresa = get_object_or_404(EmpresaCliente, id=request.POST['id'])
        
        # Verificar permisos
        if not request.user.is_superuser:
            try:
                miembro = Miembro.objects.get(usuario=request.user)
                if miembro.empresa.id != empresa.id:
                    messages.error(request, 'No tienes permisos para editar esta empresa.')
                    return redirect('empresa_lista')
            except Miembro.DoesNotExist:
                messages.error(request, 'No tienes permisos para editar empresas.')
                return redirect('empresa_lista')
        
        empresa.nombre = request.POST['nombre']
        empresa.ruc = request.POST['ruc']
        empresa.telefono = request.POST['telefono']
        empresa.email = request.POST['email']
        empresa.direccion = request.POST['direccion']
        empresa.plan = request.POST['plan']
        empresa.activo = 'activo' in request.POST
        
        nuevo_logo = request.FILES.get('logo')
        if nuevo_logo:
            if empresa.logo and os.path.isfile(empresa.logo.path):
                os.remove(empresa.logo.path)
            empresa.logo = nuevo_logo
        
        empresa.save()
        messages.success(request, 'Empresa actualizada correctamente.')
        return redirect('empresa_lista')


@login_required
def eliminar_empresa(request, id):
    # Solo administradores pueden eliminar empresas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar empresas.')
        return redirect('empresa_lista')
    
    empresa = get_object_or_404(EmpresaCliente, id=id)
    if empresa.logo and os.path.isfile(empresa.logo.path):
        os.remove(empresa.logo.path)
    empresa.delete()
    messages.success(request, 'Empresa eliminada correctamente.')
    return redirect('empresa_lista')


# ==================== CRUD MIEMBROS ====================

@login_required
def miembro_lista(request, empresa_id):
    empresa = get_object_or_404(EmpresaCliente, id=empresa_id)
    miembros = Miembro.objects.filter(empresa=empresa)
    return render(request, 'miembros/listado.html', {'miembros': miembros, 'empresa': empresa})


@login_required
def nuevo_miembro(request, empresa_id):
    empresa = get_object_or_404(EmpresaCliente, id=empresa_id)
    return render(request, 'miembros/nuevo.html', {'empresa': empresa})


@login_required
def guardar_miembro(request, empresa_id):
    if request.method == 'POST':
        empresa = get_object_or_404(EmpresaCliente, id=empresa_id)
        Miembro.objects.create(
            empresa=empresa,
            cedula=request.POST['cedula'],
            nombre=request.POST['nombre'],
            apellido=request.POST['apellido'],
            email=request.POST['email'],
            telefono=request.POST['telefono'],
            cargo=request.POST['cargo'],
            fecha_ingreso=request.POST['fecha_ingreso'],
            foto=request.FILES.get('foto'),
            activo='activo' in request.POST
        )
        messages.success(request, 'Miembro guardado correctamente.')
        return redirect('miembro_lista', empresa_id=empresa_id)


@login_required
def editar_miembro(request, id):
    miembro = get_object_or_404(Miembro, id=id)
    return render(request, 'miembros/editar.html', {'miembro': miembro})


@login_required
def procesar_edicion_miembro(request):
    if request.method == 'POST':
        miembro = get_object_or_404(Miembro, id=request.POST['id'])
        miembro.cedula = request.POST['cedula']
        miembro.nombre = request.POST['nombre']
        miembro.apellido = request.POST['apellido']
        miembro.email = request.POST['email']
        miembro.telefono = request.POST['telefono']
        miembro.cargo = request.POST['cargo']
        miembro.fecha_ingreso = request.POST['fecha_ingreso']
        miembro.activo = 'activo' in request.POST
        
        nueva_foto = request.FILES.get('foto')
        if nueva_foto:
            if miembro.foto and os.path.isfile(miembro.foto.path):
                os.remove(miembro.foto.path)
            miembro.foto = nueva_foto
        
        miembro.save()
        messages.success(request, 'Miembro actualizado correctamente.')
        return redirect('miembro_lista', empresa_id=miembro.empresa.id)


@login_required
def eliminar_miembro(request, id):
    miembro = get_object_or_404(Miembro, id=id)
    empresa_id = miembro.empresa.id
    if miembro.foto and os.path.isfile(miembro.foto.path):
        os.remove(miembro.foto.path)
    miembro.delete()
    messages.success(request, 'Miembro eliminado correctamente.')
    return redirect('miembro_lista', empresa_id=empresa_id)


# ==================== CRUD SALAS DE REUNIÓN ====================

def sala_lista(request):
    # Vista pública - Todos pueden ver las salas disponibles
    salas = SalaReunion.objects.all()
    return render(request, 'salas/listado.html', {'salas': salas})


@login_required
def nueva_sala(request):
    # Solo administradores pueden crear salas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear salas.')
        return redirect('sala_lista')
    return render(request, 'salas/nuevo.html')


@login_required
def guardar_sala(request):
    # Solo administradores pueden crear salas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear salas.')
        return redirect('sala_lista')
    
    if request.method == 'POST':
        SalaReunion.objects.create(
            nombre=request.POST['nombre'],
            capacidad=request.POST['capacidad'],
            metros_cuadrados=request.POST['metros_cuadrados'],
            piso=request.POST['piso'],
            precio_hora=request.POST['precio_hora'],
            equipamiento=request.POST['equipamiento'],
            foto=request.FILES.get('foto'),
            activo='activo' in request.POST
        )
        messages.success(request, 'Sala guardada correctamente.')
        return redirect('sala_lista')


@login_required
def editar_sala(request, id):
    # Solo administradores pueden editar salas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar salas.')
        return redirect('sala_lista')
    
    sala = get_object_or_404(SalaReunion, id=id)
    return render(request, 'salas/editar.html', {'sala': sala})


@login_required
def procesar_edicion_sala(request):
    # Solo administradores pueden editar salas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar salas.')
        return redirect('sala_lista')
    
    if request.method == 'POST':
        sala = get_object_or_404(SalaReunion, id=request.POST['id'])
        sala.nombre = request.POST.get('nombre', sala.nombre)
        sala.capacidad = request.POST.get('capacidad', sala.capacidad) if request.POST.get('capacidad') else sala.capacidad
        sala.metros_cuadrados = request.POST.get('metros_cuadrados', sala.metros_cuadrados) if request.POST.get('metros_cuadrados') else sala.metros_cuadrados
        sala.piso = request.POST.get('piso', sala.piso) if request.POST.get('piso') else sala.piso
        sala.precio_hora = request.POST.get('precio_hora', sala.precio_hora) if request.POST.get('precio_hora') else sala.precio_hora
        sala.equipamiento = request.POST.get('equipamiento', sala.equipamiento)
        sala.activo = 'activo' in request.POST
        
        nueva_foto = request.FILES.get('foto')
        if nueva_foto:
            if sala.foto and os.path.isfile(sala.foto.path):
                os.remove(sala.foto.path)
            sala.foto = nueva_foto
        
        sala.save()
        messages.success(request, 'Sala actualizada correctamente.')
        return redirect('sala_lista')


@login_required
def eliminar_sala(request, id):
    # Solo administradores pueden eliminar salas
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar salas.')
        return redirect('sala_lista')
    
    sala = get_object_or_404(SalaReunion, id=id)
    if sala.foto and os.path.isfile(sala.foto.path):
        os.remove(sala.foto.path)
    sala.delete()
    messages.success(request, 'Sala eliminada correctamente.')
    return redirect('sala_lista')


# ==================== CRUD ESCRITORIOS DEDICADOS ====================

@login_required
@login_required
def escritorio_lista(request):
    if request.user.is_superuser:
        # Administrador ve todos los escritorios
        escritorios = EscritorioDedicado.objects.all().order_by('piso', 'codigo')
    else:
        # Usuario normal ve solo escritorios de su empresa
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            # Obtener escritorios ocupados por miembros de su empresa
            miembros_empresa = Miembro.objects.filter(empresa=miembro.empresa)
            escritorios = EscritorioDedicado.objects.filter(
                miembro_asignado__in=miembros_empresa
            ).order_by('piso', 'codigo')
        except Miembro.DoesNotExist:
            escritorios = EscritorioDedicado.objects.none()
            messages.warning(request, 'No tienes una empresa asociada.')
    return render(request, 'escritorios/listado.html', {'escritorios': escritorios})


@login_required
def escritorio_mapa(request):
    if request.user.is_superuser:
        escritorios = EscritorioDedicado.objects.all()
        miembros = Miembro.objects.filter(activo=True)
    else:
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            miembros_empresa = Miembro.objects.filter(empresa=miembro.empresa, activo=True)
            escritorios = EscritorioDedicado.objects.filter(miembro_asignado__in=miembros_empresa)
            miembros = miembros_empresa
        except Miembro.DoesNotExist:
            escritorios = EscritorioDedicado.objects.none()
            miembros = Miembro.objects.none()
            messages.warning(request, 'No tienes una empresa asociada.')
    
    pisos = escritorios.values_list('piso', flat=True).distinct().order_by('piso')
    piso_seleccionado = request.GET.get('piso', pisos.first() if pisos.exists() else 1)
    escritorios_piso = escritorios.filter(piso=piso_seleccionado)
    
    return render(request, 'escritorios/mapa.html', {
        'escritorios': escritorios_piso,
        'pisos': pisos,
        'piso_seleccionado': int(piso_seleccionado) if piso_seleccionado else 1,
        'miembros': miembros,
    })


@login_required
def nuevo_escritorio(request):
    # Solo administradores pueden crear escritorios
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear escritorios.')
        return redirect('escritorio_lista')
    
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'escritorios/nuevo.html', {'miembros': miembros})


@login_required
def guardar_escritorio(request):
    # Solo administradores pueden crear escritorios
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para crear escritorios.')
        return redirect('escritorio_lista')
    
    if request.method == 'POST':
        miembro_id = request.POST.get('miembro_asignado')
        miembro = Miembro.objects.get(id=miembro_id) if miembro_id else None
        
        piso = int(request.POST['piso'])
        
        # Buscar la primera posición disponible (1-10) en el piso seleccionado
        posicion = None
        for pos in range(1, 11):  # Posiciones 1 a 10
            if not EscritorioDedicado.objects.filter(piso=piso, posicion=pos).exists():
                posicion = pos
                break
        
        if posicion is None:
            messages.error(request, f'El Piso {piso} está lleno. Máximo 10 escritorios por piso.')
            return redirect('nuevo_escritorio')
        
        EscritorioDedicado.objects.create(
            codigo=request.POST['codigo'],
            piso=piso,
            posicion=posicion,
            precio_mensual=request.POST['precio_mensual'],
            tipo=request.POST['tipo'],
            estado=request.POST['estado'],
            miembro_asignado=miembro
        )
        messages.success(request, f'Escritorio guardado en Piso {piso}, Posición {posicion}. Puedes reorganizar desde el mapa.')
        return redirect('escritorio_lista')


@login_required
def editar_escritorio(request, id):
    escritorio = get_object_or_404(EscritorioDedicado, id=id)
    
    # Verificar permisos
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar escritorios.')
        return redirect('escritorio_lista')
    
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'escritorios/editar.html', {'escritorio': escritorio, 'miembros': miembros})


@login_required
def procesar_edicion_escritorio(request):
    # Solo administradores pueden editar escritorios
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para editar escritorios.')
        return redirect('escritorio_lista')
    
    if request.method == 'POST':
        escritorio = get_object_or_404(EscritorioDedicado, id=request.POST['id'])
        miembro_anterior = escritorio.miembro_asignado  # Guardar miembro anterior
        
        escritorio.codigo = request.POST['codigo']
        escritorio.piso = int(request.POST['piso'])
        escritorio.precio_mensual = request.POST['precio_mensual']
        escritorio.tipo = request.POST['tipo']
        escritorio.estado = request.POST['estado']
        
        # Las posiciones NO se editan aquí, solo desde el mapa arrastrando
        # Mantener posiciones actuales
        
        miembro_id = request.POST.get('miembro_asignado')
        miembro_nuevo = Miembro.objects.get(id=miembro_id) if miembro_id else None
        escritorio.miembro_asignado = miembro_nuevo
        
        escritorio.save()
        
        # Si se asignó un nuevo miembro (y no era el mismo), enviar PDF
        if miembro_nuevo and miembro_nuevo != miembro_anterior:
            try:
                pdf_bytes = _generar_pdf_escritorio(escritorio)
                asunto = f'CoworkSpace KC - Escritorio Asignado: {escritorio.codigo}'
                mensaje_texto = f'''Hola {miembro_nuevo.nombre} {miembro_nuevo.apellido},

Se te ha asignado un escritorio dedicado.

Detalle:
- Código: {escritorio.codigo}
- Piso: {escritorio.piso}
- Posición: {escritorio.posicion}
- Tipo: {escritorio.get_tipo_display()}
- Precio Mensual: ${escritorio.precio_mensual}

Adjunto encontrarás los detalles en PDF.

Saludos,
CoworkSpace KC
'''
                mensaje_html = f'''<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;border:1px solid #eee;border-radius:8px;">
<div style="background:#4A6785;padding:28px;text-align:center;">
<h1 style="color:#fff;margin:0;font-size:26px;">CoworkSpace KC</h1>
<p style="color:rgba(255,255,255,.85);margin:6px 0 0;">Escritorio Asignado</p>
</div>
<div style="padding:32px;">
<h2 style="color:#1F1F1F;">¡Escritorio Dedicado Asignado!</h2>
<p>Hola <strong>{miembro_nuevo.nombre} {miembro_nuevo.apellido}</strong>,</p>
<div style="background:#f9f9f9;border-radius:8px;padding:20px;margin:20px 0;">
<table style="width:100%;">
<tr><td style="padding:6px 0;color:#888;">Código:</td><td style="font-weight:bold;">{escritorio.codigo}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Ubicación:</td><td>Piso {escritorio.piso}, Posición {escritorio.posicion}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Tipo:</td><td>{escritorio.get_tipo_display()}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Precio:</td><td style="font-weight:bold;color:#4A6785;">${escritorio.precio_mensual}/mes</td></tr>
</table>
</div>
<p style="color:#777;font-size:13px;text-align:center;border-top:1px solid #eee;padding-top:20px;">CoworkSpace KC</p>
</div>
</div>'''
                _enviar_email_con_pdf(
                    miembro_nuevo.email,
                    asunto,
                    mensaje_texto,
                    mensaje_html,
                    pdf_bytes,
                    f'Escritorio_{escritorio.codigo}.pdf'
                )
                messages.success(request, f'Escritorio asignado y confirmación enviada a {miembro_nuevo.email}')
            except Exception as e:
                print(f'Error generando/enviando PDF: {e}')
                messages.success(request, 'Escritorio actualizado correctamente.')
        else:
            messages.success(request, 'Escritorio actualizado correctamente.')
        
        return redirect('escritorio_lista')


@login_required
@login_required
def eliminar_escritorio(request, id):
    # Solo administradores pueden eliminar escritorios
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para eliminar escritorios.')
        return redirect('escritorio_lista')
    
    escritorio = get_object_or_404(EscritorioDedicado, id=id)
    escritorio.delete()
    messages.success(request, 'Escritorio eliminado correctamente.')
    return redirect('escritorio_lista')


@login_required
def actualizar_posicion_escritorio(request):
    # Solo administradores pueden mover escritorios
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'No tienes permisos para mover escritorios'})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        escritorio_id = data.get('id')
        nueva_posicion = data.get('posicion')  # Nueva posición horizontal 1-10
        
        escritorio = get_object_or_404(EscritorioDedicado, id=escritorio_id)
        
        # Validar que la nueva posición esté en rango 1-10
        if not (1 <= nueva_posicion <= 10):
            return JsonResponse({'success': False, 'error': 'Posición debe estar entre 1 y 10'})
        
        # Verificar si la posición está ocupada por otro escritorio en el mismo piso
        if EscritorioDedicado.objects.filter(piso=escritorio.piso, posicion=nueva_posicion).exclude(id=escritorio_id).exists():
            return JsonResponse({'success': False, 'error': 'Posición ya ocupada'})
        
        escritorio.posicion = nueva_posicion
        escritorio.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


@login_required
def intercambiar_escritorios(request):
    # Solo administradores pueden intercambiar escritorios
    if not request.user.is_superuser:
        return JsonResponse({'success': False, 'error': 'No tienes permisos para intercambiar escritorios'})
    
    if request.method == 'POST':
        data = json.loads(request.body)
        escritorio1_id = data.get('escritorio1_id')
        escritorio2_id = data.get('escritorio2_id')
        posicion1 = data.get('posicion1')
        posicion2 = data.get('posicion2')
        
        escritorio1 = get_object_or_404(EscritorioDedicado, id=escritorio1_id)
        escritorio2 = get_object_or_404(EscritorioDedicado, id=escritorio2_id)
        
        # Validar que ambos estén en el mismo piso
        if escritorio1.piso != escritorio2.piso:
            return JsonResponse({'success': False, 'message': 'Los escritorios deben estar en el mismo piso'})
        
        # Intercambiar las posiciones
        escritorio1.posicion = posicion2
        escritorio2.posicion = posicion1
        
        escritorio1.save()
        escritorio2.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})


# ==================== CRUD RESERVAS DE SALAS ====================

@login_required
def reserva_lista(request):
    if request.user.is_superuser:
        reservas = ReservaSala.objects.all().order_by('-fecha', '-hora_inicio')
    else:
        # Usuario normal ve solo sus reservas (si tiene miembro asociado)
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            reservas = ReservaSala.objects.filter(miembro=miembro).order_by('-fecha', '-hora_inicio')
        except:
            reservas = ReservaSala.objects.none()
    return render(request, 'reservas/listado.html', {'reservas': reservas})


@login_required
def reserva_calendario(request):
    salas = SalaReunion.objects.filter(activo=True)
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'reservas/calendario.html', {'salas': salas, 'miembros': miembros})


@login_required
def reservas_api(request):
    """API para FullCalendar - devuelve las reservas en formato JSON"""
    reservas = ReservaSala.objects.all()
    eventos = []
    
    for reserva in reservas:
        color = '#28a745' if reserva.estado == 'confirmada' else '#6c757d'
        if reserva.estado == 'cancelada':
            color = '#dc3545'
        
        eventos.append({
            'id': reserva.id,
            'title': f"{reserva.sala.nombre} - {reserva.miembro.nombre}",
            'start': f"{reserva.fecha}T{reserva.hora_inicio}",
            'end': f"{reserva.fecha}T{reserva.hora_fin}",
            'backgroundColor': color,
            'borderColor': color,
            'extendedProps': {
                'sala': reserva.sala.nombre,
                'miembro': f"{reserva.miembro.nombre} {reserva.miembro.apellido}",
                'proposito': reserva.proposito,
                'estado': reserva.estado,
            }
        })
    
    return JsonResponse(eventos, safe=False)


@login_required
def nueva_reserva(request):
    salas = SalaReunion.objects.filter(activo=True)
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'reservas/nuevo.html', {'salas': salas, 'miembros': miembros})


@login_required
def guardar_reserva(request):
    if request.method == 'POST':
        sala = get_object_or_404(SalaReunion, id=request.POST['sala'])
        miembro = get_object_or_404(Miembro, id=request.POST['miembro'])
        
        # Obtener fecha y horas
        fecha = request.POST['fecha']
        hora_inicio = datetime.strptime(request.POST['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.POST['hora_fin'], '%H:%M').time()
        
        # Validar que hora_fin sea mayor que hora_inicio
        if hora_fin <= hora_inicio:
            messages.error(request, 'La hora de fin debe ser mayor que la hora de inicio.')
            return redirect('nueva_reserva')
        
        # VALIDACIÓN: Verificar si ya existe una reserva que se solapa en el mismo día y sala
        reservas_existentes = ReservaSala.objects.filter(
            sala=sala,
            fecha=fecha,
            estado__in=['confirmada', 'pendiente']  # Solo validar reservas activas
        )
        
        for reserva in reservas_existentes:
            # Verificar solapamiento de horarios
            # Hay solapamiento si:
            # - La nueva hora_inicio está entre hora_inicio y hora_fin de la reserva existente
            # - La nueva hora_fin está entre hora_inicio y hora_fin de la reserva existente
            # - La nueva reserva envuelve completamente a la existente
            if (reserva.hora_inicio <= hora_inicio < reserva.hora_fin) or \
               (reserva.hora_inicio < hora_fin <= reserva.hora_fin) or \
               (hora_inicio <= reserva.hora_inicio and hora_fin >= reserva.hora_fin):
                messages.error(request, 
                    f'La sala ya está reservada en ese horario. '
                    f'Reserva existente: {reserva.hora_inicio.strftime("%H:%M")} - {reserva.hora_fin.strftime("%H:%M")} '
                    f'por {reserva.miembro.nombre} {reserva.miembro.apellido}')
                return redirect('nueva_reserva')
        
        # Calcular costo total (diferencia de horas * precio por hora)
        horas = (datetime.combine(date.today(), hora_fin) - datetime.combine(date.today(), hora_inicio)).seconds / 3600
        costo_total = Decimal(horas) * sala.precio_hora
        
        reserva = ReservaSala.objects.create(
            sala=sala,
            miembro=miembro,
            fecha=fecha,
            hora_inicio=request.POST['hora_inicio'],
            hora_fin=request.POST['hora_fin'],
            proposito=request.POST['proposito'],
            numero_asistentes=request.POST['numero_asistentes'],
            estado=request.POST.get('estado', 'confirmada'),
            costo_total=costo_total
        )
        
        # Generar y enviar PDF por correo
        try:
            pdf_bytes = _generar_pdf_reserva(reserva)
            asunto = f'CoworkSpace KC - Reserva Confirmada: {sala.nombre}'
            mensaje_texto = f'''Hola {miembro.nombre} {miembro.apellido},

Tu reserva ha sido confirmada exitosamente.

Detalle:
- Sala: {sala.nombre}
- Fecha: {reserva.fecha.strftime("%d/%m/%Y")}
- Hora: {reserva.hora_inicio.strftime("%H:%M")} - {reserva.hora_fin.strftime("%H:%M")}
- Propósito: {reserva.proposito}
- Asistentes: {reserva.numero_asistentes}
- Costo: ${reserva.costo_total}

Adjunto encontrarás la confirmación en PDF.

Saludos,
CoworkSpace KC
'''
            mensaje_html = f'''<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;border:1px solid #eee;border-radius:8px;">
<div style="background:#4A6785;padding:28px;text-align:center;">
<h1 style="color:#fff;margin:0;font-size:26px;">CoworkSpace KC</h1>
<p style="color:rgba(255,255,255,.85);margin:6px 0 0;">Reserva Confirmada</p>
</div>
<div style="padding:32px;">
<h2 style="color:#1F1F1F;">¡Reserva Exitosa!</h2>
<p>Hola <strong>{miembro.nombre} {miembro.apellido}</strong>,</p>
<div style="background:#f9f9f9;border-radius:8px;padding:20px;margin:20px 0;">
<table style="width:100%;">
<tr><td style="padding:6px 0;color:#888;">Sala:</td><td style="font-weight:bold;">{sala.nombre}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Fecha:</td><td>{reserva.fecha.strftime("%d/%m/%Y")}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Hora:</td><td>{reserva.hora_inicio.strftime("%H:%M")} - {reserva.hora_fin.strftime("%H:%M")}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Costo:</td><td style="font-weight:bold;color:#4A6785;">${reserva.costo_total}</td></tr>
</table>
</div>
<p style="color:#777;font-size:13px;text-align:center;border-top:1px solid #eee;padding-top:20px;">CoworkSpace KC</p>
</div>
</div>'''
            _enviar_email_con_pdf(
                miembro.email,
                asunto,
                mensaje_texto,
                mensaje_html,
                pdf_bytes,
                f'Reserva_{sala.nombre}_{reserva.fecha.strftime("%Y%m%d")}.pdf'
            )
            messages.success(request, f'Reserva confirmada y enviada a {miembro.email}')
        except Exception as e:
            print(f'Error generando/enviando PDF: {e}')
            messages.success(request, 'Reserva guardada correctamente.')
        
        return redirect('reserva_lista')


@login_required
def editar_reserva(request, id):
    reserva = get_object_or_404(ReservaSala, id=id)
    salas = SalaReunion.objects.filter(activo=True)
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'reservas/editar.html', {'reserva': reserva, 'salas': salas, 'miembros': miembros})


@login_required
def procesar_edicion_reserva(request):
    if request.method == 'POST':
        reserva = get_object_or_404(ReservaSala, id=request.POST['id'])
        sala = get_object_or_404(SalaReunion, id=request.POST['sala'])
        miembro = get_object_or_404(Miembro, id=request.POST['miembro'])
        
        # Obtener fecha y horas
        fecha = request.POST['fecha']
        hora_inicio = datetime.strptime(request.POST['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.POST['hora_fin'], '%H:%M').time()
        
        # Validar que hora_fin sea mayor que hora_inicio
        if hora_fin <= hora_inicio:
            messages.error(request, 'La hora de fin debe ser mayor que la hora de inicio.')
            return redirect('editar_reserva', id=reserva.id)
        
        # VALIDACIÓN: Verificar si ya existe una reserva que se solapa (excluyendo la reserva actual)
        reservas_existentes = ReservaSala.objects.filter(
            sala=sala,
            fecha=fecha,
            estado__in=['confirmada', 'pendiente']
        ).exclude(id=reserva.id)  # Excluir la reserva actual
        
        for reserva_existente in reservas_existentes:
            # Verificar solapamiento de horarios
            if (reserva_existente.hora_inicio <= hora_inicio < reserva_existente.hora_fin) or \
               (reserva_existente.hora_inicio < hora_fin <= reserva_existente.hora_fin) or \
               (hora_inicio <= reserva_existente.hora_inicio and hora_fin >= reserva_existente.hora_fin):
                messages.error(request, 
                    f'La sala ya está reservada en ese horario. '
                    f'Reserva existente: {reserva_existente.hora_inicio.strftime("%H:%M")} - {reserva_existente.hora_fin.strftime("%H:%M")} '
                    f'por {reserva_existente.miembro.nombre} {reserva_existente.miembro.apellido}')
                return redirect('editar_reserva', id=reserva.id)
        
        # Recalcular costo
        horas = (datetime.combine(date.today(), hora_fin) - datetime.combine(date.today(), hora_inicio)).seconds / 3600
        costo_total = Decimal(horas) * sala.precio_hora
        
        reserva.sala = sala
        reserva.miembro = miembro
        reserva.fecha = request.POST['fecha']
        reserva.hora_inicio = request.POST['hora_inicio']
        reserva.hora_fin = request.POST['hora_fin']
        reserva.proposito = request.POST['proposito']
        reserva.numero_asistentes = request.POST['numero_asistentes']
        reserva.estado = request.POST.get('estado', 'confirmada')
        reserva.costo_total = costo_total
        reserva.save()
        
        messages.success(request, 'Reserva actualizada correctamente.')
        return redirect('reserva_lista')


@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(ReservaSala, id=id)
    reserva.delete()
    messages.success(request, 'Reserva eliminada correctamente.')
    return redirect('reserva_lista')


# ==================== CRUD EVENTOS ====================

def evento_lista(request):
    # Vista pública - Todos pueden ver los eventos (especialmente los públicos)
    eventos = Evento.objects.all().order_by('-fecha_evento')
    return render(request, 'eventos/listado.html', {'eventos': eventos})


@login_required
def nuevo_evento(request):
    empresas = EmpresaCliente.objects.filter(activo=True)
    salas = SalaReunion.objects.filter(activo=True)
    return render(request, 'eventos/nuevo.html', {'empresas': empresas, 'salas': salas})


@login_required
def guardar_evento(request):
    if request.method == 'POST':
        organizador = get_object_or_404(EmpresaCliente, id=request.POST['organizador'])
        sala_id = request.POST.get('sala')
        sala = SalaReunion.objects.get(id=sala_id) if sala_id else None
        
        # Obtener fecha y horas
        fecha_evento = request.POST['fecha_evento']
        hora_inicio = datetime.strptime(request.POST['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.POST['hora_fin'], '%H:%M').time()
        
        # Validar que hora_fin sea mayor que hora_inicio
        if hora_fin <= hora_inicio:
            messages.error(request, 'La hora de fin debe ser mayor que la hora de inicio.')
            return redirect('nuevo_evento')
        
        # VALIDACIÓN: Si el evento usa una sala, verificar solapamiento con reservas y eventos existentes
        if sala:
            # Verificar solapamiento con otros eventos en la misma sala
            eventos_existentes = Evento.objects.filter(
                sala=sala,
                fecha_evento=fecha_evento
            )
            
            for evento in eventos_existentes:
                # Verificar solapamiento de horarios
                if (evento.hora_inicio <= hora_inicio < evento.hora_fin) or \
                   (evento.hora_inicio < hora_fin <= evento.hora_fin) or \
                   (hora_inicio <= evento.hora_inicio and hora_fin >= evento.hora_fin):
                    messages.error(request, 
                        f'La sala ya está ocupada con otro evento en ese horario. '
                        f'Evento existente: "{evento.titulo}" de {evento.hora_inicio.strftime("%H:%M")} - {evento.hora_fin.strftime("%H:%M")}')
                    return redirect('nuevo_evento')
            
            # Verificar solapamiento con reservas normales de la sala
            reservas_existentes = ReservaSala.objects.filter(
                sala=sala,
                fecha=fecha_evento,
                estado__in=['confirmada', 'pendiente']
            )
            
            for reserva in reservas_existentes:
                # Verificar solapamiento de horarios
                if (reserva.hora_inicio <= hora_inicio < reserva.hora_fin) or \
                   (reserva.hora_inicio < hora_fin <= reserva.hora_fin) or \
                   (hora_inicio <= reserva.hora_inicio and hora_fin >= reserva.hora_fin):
                    messages.error(request, 
                        f'La sala ya está reservada en ese horario. '
                        f'Reserva existente: {reserva.hora_inicio.strftime("%H:%M")} - {reserva.hora_fin.strftime("%H:%M")} '
                        f'por {reserva.miembro.nombre} {reserva.miembro.apellido}')
                    return redirect('nuevo_evento')
        
        evento = Evento.objects.create(
            titulo=request.POST['titulo'],
            descripcion=request.POST['descripcion'],
            organizador=organizador,
            fecha_evento=fecha_evento,
            hora_inicio=request.POST['hora_inicio'],
            hora_fin=request.POST['hora_fin'],
            sala=sala,
            capacidad_maxima=request.POST['capacidad_maxima'],
            tipo_evento=request.POST['tipo_evento'],
            publico='publico' in request.POST,
            foto=request.FILES.get('foto')
        )
        
        # Generar y enviar PDF por correo
        try:
            pdf_bytes = _generar_pdf_evento(evento)
            asunto = f'CoworkSpace KC - Evento Registrado: {evento.titulo}'
            mensaje_texto = f'''Hola {organizador.nombre},

Tu evento ha sido registrado exitosamente.

Detalle:
- Título: {evento.titulo}
- Fecha: {evento.fecha_evento.strftime("%d/%m/%Y")}
- Hora: {evento.hora_inicio.strftime("%H:%M")} - {evento.hora_fin.strftime("%H:%M")}
- Sala: {sala.nombre if sala else 'Sin sala asignada'}
- Tipo: {evento.get_tipo_evento_display()}
- Capacidad: {evento.capacidad_maxima} personas

Adjunto encontrarás la confirmación en PDF.

Saludos,
CoworkSpace KC
'''
            mensaje_html = f'''<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;border:1px solid #eee;border-radius:8px;">
<div style="background:#4A6785;padding:28px;text-align:center;">
<h1 style="color:#fff;margin:0;font-size:26px;">CoworkSpace KC</h1>
<p style="color:rgba(255,255,255,.85);margin:6px 0 0;">Evento Registrado</p>
</div>
<div style="padding:32px;">
<h2 style="color:#1F1F1F;">¡Evento Confirmado!</h2>
<p>Hola <strong>{organizador.nombre}</strong>,</p>
<div style="background:#f9f9f9;border-radius:8px;padding:20px;margin:20px 0;">
<table style="width:100%;">
<tr><td style="padding:6px 0;color:#888;">Evento:</td><td style="font-weight:bold;">{evento.titulo}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Fecha:</td><td>{evento.fecha_evento.strftime("%d/%m/%Y")}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Hora:</td><td>{evento.hora_inicio.strftime("%H:%M")} - {evento.hora_fin.strftime("%H:%M")}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Sala:</td><td>{sala.nombre if sala else 'Sin sala'}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Capacidad:</td><td>{evento.capacidad_maxima} personas</td></tr>
</table>
</div>
<p style="color:#777;font-size:13px;text-align:center;border-top:1px solid #eee;padding-top:20px;">CoworkSpace KC</p>
</div>
</div>'''
            _enviar_email_con_pdf(
                organizador.email,
                asunto,
                mensaje_texto,
                mensaje_html,
                pdf_bytes,
                f'Evento_{evento.titulo.replace(" ", "_")}_{evento.fecha_evento.strftime("%Y%m%d")}.pdf'
            )
            messages.success(request, f'Evento registrado y confirmación enviada a {organizador.email}')
        except Exception as e:
            print(f'Error generando/enviando PDF: {e}')
            messages.success(request, 'Evento guardado correctamente.')
        
        return redirect('evento_lista')


@login_required
def editar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    empresas = EmpresaCliente.objects.filter(activo=True)
    salas = SalaReunion.objects.filter(activo=True)
    return render(request, 'eventos/editar.html', {'evento': evento, 'empresas': empresas, 'salas': salas})


@login_required
def procesar_edicion_evento(request):
    if request.method == 'POST':
        evento = get_object_or_404(Evento, id=request.POST['id'])
        organizador = get_object_or_404(EmpresaCliente, id=request.POST['organizador'])
        sala_id = request.POST.get('sala')
        sala = SalaReunion.objects.get(id=sala_id) if sala_id else None
        
        # Obtener fecha y horas
        fecha_evento = request.POST['fecha_evento']
        hora_inicio = datetime.strptime(request.POST['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.POST['hora_fin'], '%H:%M').time()
        
        # Validar que hora_fin sea mayor que hora_inicio
        if hora_fin <= hora_inicio:
            messages.error(request, 'La hora de fin debe ser mayor que la hora de inicio.')
            return redirect('editar_evento', id=evento.id)
        
        # VALIDACIÓN: Si el evento usa una sala, verificar solapamiento (excluyendo el evento actual)
        if sala:
            # Verificar solapamiento con otros eventos en la misma sala
            eventos_existentes = Evento.objects.filter(
                sala=sala,
                fecha_evento=fecha_evento
            ).exclude(id=evento.id)  # Excluir el evento actual
            
            for evento_existente in eventos_existentes:
                # Verificar solapamiento de horarios
                if (evento_existente.hora_inicio <= hora_inicio < evento_existente.hora_fin) or \
                   (evento_existente.hora_inicio < hora_fin <= evento_existente.hora_fin) or \
                   (hora_inicio <= evento_existente.hora_inicio and hora_fin >= evento_existente.hora_fin):
                    messages.error(request, 
                        f'La sala ya está ocupada con otro evento en ese horario. '
                        f'Evento existente: "{evento_existente.titulo}" de {evento_existente.hora_inicio.strftime("%H:%M")} - {evento_existente.hora_fin.strftime("%H:%M")}')
                    return redirect('editar_evento', id=evento.id)
            
            # Verificar solapamiento con reservas normales de la sala
            reservas_existentes = ReservaSala.objects.filter(
                sala=sala,
                fecha=fecha_evento,
                estado__in=['confirmada', 'pendiente']
            )
            
            for reserva in reservas_existentes:
                # Verificar solapamiento de horarios
                if (reserva.hora_inicio <= hora_inicio < reserva.hora_fin) or \
                   (reserva.hora_inicio < hora_fin <= reserva.hora_fin) or \
                   (hora_inicio <= reserva.hora_inicio and hora_fin >= reserva.hora_fin):
                    messages.error(request, 
                        f'La sala ya está reservada en ese horario. '
                        f'Reserva existente: {reserva.hora_inicio.strftime("%H:%M")} - {reserva.hora_fin.strftime("%H:%M")} '
                        f'por {reserva.miembro.nombre} {reserva.miembro.apellido}')
                    return redirect('editar_evento', id=evento.id)
        
        evento.titulo = request.POST['titulo']
        evento.descripcion = request.POST['descripcion']
        evento.organizador = organizador
        evento.fecha_evento = fecha_evento
        evento.hora_inicio = request.POST['hora_inicio']
        evento.hora_fin = request.POST['hora_fin']
        evento.sala = sala
        evento.capacidad_maxima = request.POST['capacidad_maxima']
        evento.tipo_evento = request.POST['tipo_evento']
        evento.publico = 'publico' in request.POST
        
        nueva_foto = request.FILES.get('foto')
        if nueva_foto:
            if evento.foto and os.path.isfile(evento.foto.path):
                os.remove(evento.foto.path)
            evento.foto = nueva_foto
        
        evento.save()
        messages.success(request, 'Evento actualizado correctamente.')
        return redirect('evento_lista')


@login_required
def eliminar_evento(request, id):
    evento = get_object_or_404(Evento, id=id)
    if evento.foto and os.path.isfile(evento.foto.path):
        os.remove(evento.foto.path)
    evento.delete()
    messages.success(request, 'Evento eliminado correctamente.')
    return redirect('evento_lista')


# ==================== CRUD FACTURAS ====================

@login_required
def factura_lista(request):
    if request.user.is_superuser:
        facturas = Factura.objects.all().order_by('-fecha_emision')
    else:
        facturas = Factura.objects.filter(estado='pendiente').order_by('-fecha_emision')
    return render(request, 'facturas/listado.html', {'facturas': facturas})


@login_required
def nueva_factura(request):
    empresas = EmpresaCliente.objects.filter(activo=True)
    return render(request, 'facturas/nuevo.html', {'empresas': empresas})


@login_required
def guardar_factura(request):
    if request.method == 'POST':
        empresa = get_object_or_404(EmpresaCliente, id=request.POST['empresa'])
        subtotal = Decimal(request.POST['subtotal'])
        iva = subtotal * Decimal('0.15')  # IVA 15%
        total = subtotal + iva
        
        factura = Factura.objects.create(
            empresa=empresa,
            fecha_vencimiento=request.POST['fecha_vencimiento'],
            subtotal=subtotal,
            iva=iva,
            total=total,
            tipo_factura=request.POST['tipo_factura'],
            estado=request.POST.get('estado', 'pendiente'),
            notas=request.POST.get('notas', ''),
            pdf=request.FILES.get('pdf')
        )
        
        # Generar y enviar PDF por correo
        try:
            pdf_bytes = _generar_pdf_factura(factura)
            asunto = f'CoworkSpace KC - Factura {factura.numero_factura}'
            mensaje_texto = f'''Hola {empresa.nombre},

Se ha generado la factura {factura.numero_factura} para tu empresa.

Detalle:
- Subtotal: ${factura.subtotal}
- IVA (15%): ${factura.iva}
- Total: ${factura.total}
- Estado: {factura.get_estado_display()}
- Fecha de vencimiento: {factura.fecha_vencimiento.strftime("%d/%m/%Y")}

Adjunto encontrarás el PDF de la factura.

Saludos,
CoworkSpace KC
'''
            mensaje_html = f'''<div style="font-family:Arial,sans-serif;max-width:600px;margin:0 auto;border:1px solid #eee;border-radius:8px;">
<div style="background:#4A6785;padding:28px;text-align:center;">
<h1 style="color:#fff;margin:0;font-size:26px;">CoworkSpace KC</h1>
<p style="color:rgba(255,255,255,.85);margin:6px 0 0;">Nueva Factura Generada</p>
</div>
<div style="padding:32px;">
<h2 style="color:#1F1F1F;">Factura {factura.numero_factura}</h2>
<p>Hola <strong>{empresa.nombre}</strong>,</p>
<div style="background:#f9f9f9;border-radius:8px;padding:20px;margin:20px 0;">
<table style="width:100%;">
<tr><td style="padding:6px 0;color:#888;">Subtotal:</td><td style="font-weight:bold;">${factura.subtotal}</td></tr>
<tr><td style="padding:6px 0;color:#888;">IVA (15%):</td><td style="font-weight:bold;">${factura.iva}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Total:</td><td style="font-weight:bold;color:#4A6785;font-size:18px;">${factura.total}</td></tr>
<tr><td style="padding:6px 0;color:#888;">Vencimiento:</td><td>{factura.fecha_vencimiento.strftime("%d/%m/%Y")}</td></tr>
</table>
</div>
<p style="color:#777;font-size:13px;text-align:center;border-top:1px solid #eee;padding-top:20px;">CoworkSpace KC</p>
</div>
</div>'''
            _enviar_email_con_pdf(
                empresa.email,
                asunto,
                mensaje_texto,
                mensaje_html,
                pdf_bytes,
                f'Factura_{factura.numero_factura}.pdf'
            )
            messages.success(request, f'Factura guardada y enviada a {empresa.email}')
        except Exception as e:
            print(f'Error generando/enviando PDF: {e}')
            messages.success(request, 'Factura guardada correctamente.')
        
        return redirect('factura_lista')


@login_required
def editar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    empresas = EmpresaCliente.objects.filter(activo=True)
    return render(request, 'facturas/editar.html', {'factura': factura, 'empresas': empresas})


@login_required
def procesar_edicion_factura(request):
    if request.method == 'POST':
        factura = get_object_or_404(Factura, id=request.POST['id'])
        empresa = get_object_or_404(EmpresaCliente, id=request.POST['empresa'])
        subtotal = Decimal(request.POST['subtotal'])
        iva = subtotal * Decimal('0.12')
        total = subtotal + iva
        
        factura.empresa = empresa
        factura.fecha_vencimiento = request.POST['fecha_vencimiento']
        factura.subtotal = subtotal
        factura.iva = iva
        factura.total = total
        factura.tipo_factura = request.POST['tipo_factura']
        factura.estado = request.POST.get('estado', 'pendiente')
        factura.notas = request.POST.get('notas', '')
        
        nuevo_pdf = request.FILES.get('pdf')
        if nuevo_pdf:
            if factura.pdf and os.path.isfile(factura.pdf.path):
                os.remove(factura.pdf.path)
            factura.pdf = nuevo_pdf
        
        factura.save()
        messages.success(request, 'Factura actualizada correctamente.')
        return redirect('factura_lista')


@login_required
def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    if factura.pdf and os.path.isfile(factura.pdf.path):
        os.remove(factura.pdf.path)
    factura.delete()
    messages.success(request, 'Factura eliminada correctamente.')
    return redirect('factura_lista')


@login_required
def generar_pdf_factura(request, id):
    """Genera un PDF básico de la factura"""
    factura = get_object_or_404(Factura, id=id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="factura_{factura.numero_factura}.pdf"'
    
    # Aquí irá la lógica de generación con reportlab cuando se necesite
    # Por ahora devolvemos un mensaje
    response.write(b'PDF de factura - Implementar con reportlab')
    
    return response


@login_required
def calcular_subtotal_automatico(request, empresa_id):
    """Calcula el subtotal automático basado en los servicios de la empresa"""
    empresa = get_object_or_404(EmpresaCliente, id=empresa_id)
    
    # Obtener mes y año actual
    fecha_actual = date.today()
    mes_actual = fecha_actual.month
    año_actual = fecha_actual.year
    
    subtotal = Decimal('0.00')
    desglose = {
        'escritorios_count': 0,
        'escritorios_total': Decimal('0.00'),
        'escritorios_promedio': Decimal('0.00'),
        'reservas_count': 0,
        'reservas_total': Decimal('0.00'),
        'eventos_count': 0,
        'eventos_total': Decimal('0.00'),
    }
    
    # 1. Calcular escritorios ocupados por miembros de esta empresa
    miembros = Miembro.objects.filter(empresa=empresa, activo=True)
    escritorios_ocupados = EscritorioDedicado.objects.filter(
        miembro_asignado__in=miembros,
        estado='ocupado'
    )
    
    if escritorios_ocupados.exists():
        desglose['escritorios_count'] = escritorios_ocupados.count()
        desglose['escritorios_total'] = sum([e.precio_mensual for e in escritorios_ocupados])
        desglose['escritorios_promedio'] = desglose['escritorios_total'] / desglose['escritorios_count']
        subtotal += desglose['escritorios_total']
    
    # 2. Calcular reservas de salas confirmadas del mes actual
    reservas_mes = ReservaSala.objects.filter(
        miembro__empresa=empresa,
        fecha__month=mes_actual,
        fecha__year=año_actual,
        estado='confirmada'
    )
    
    if reservas_mes.exists():
        desglose['reservas_count'] = reservas_mes.count()
        desglose['reservas_total'] = sum([r.costo_total for r in reservas_mes])
        subtotal += desglose['reservas_total']
    
    # 3. Calcular eventos organizados por la empresa del mes actual (si usan sala, cobrar por horas)
    eventos_mes = Evento.objects.filter(
        organizador=empresa,
        fecha_evento__month=mes_actual,
        fecha_evento__year=año_actual
    )
    
    if eventos_mes.exists():
        desglose['eventos_count'] = eventos_mes.count()
        # Calcular costo de eventos que usan salas
        for evento in eventos_mes:
            if evento.sala:
                # Calcular horas del evento
                hora_inicio = datetime.combine(date.today(), evento.hora_inicio)
                hora_fin = datetime.combine(date.today(), evento.hora_fin)
                horas = (hora_fin - hora_inicio).seconds / 3600
                costo_evento = Decimal(horas) * evento.sala.precio_hora
                desglose['eventos_total'] += costo_evento
        subtotal += desglose['eventos_total']
    
    # Verificar si hay servicios
    if subtotal > 0:
        return JsonResponse({
            'success': True,
            'subtotal': float(subtotal),
            'desglose': {
                'escritorios_count': desglose['escritorios_count'],
                'escritorios_total': float(desglose['escritorios_total']),
                'escritorios_promedio': float(desglose['escritorios_promedio']),
                'reservas_count': desglose['reservas_count'],
                'reservas_total': float(desglose['reservas_total']),
                'eventos_count': desglose['eventos_count'],
                'eventos_total': float(desglose['eventos_total']),
            }
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Esta empresa no tiene servicios facturables este mes',
            'subtotal': 0
        })


# ==================== REPORTES ====================

@login_required
def reportes(request):
    """Vista principal de reportes"""
    return render(request, 'reportes/index.html')



@login_required
def reporte_ocupacion(request):
    """Reporte de tasa de ocupación por metros cuadrados"""
    salas = SalaReunion.objects.filter(activo=True)
    escritorios = EscritorioDedicado.objects.all()
    
    # Calcular ocupación de escritorios
    total_escritorios = escritorios.count()
    escritorios_ocupados = escritorios.filter(estado='ocupado').count()
    escritorios_disponibles = escritorios.filter(estado='disponible').count()
    escritorios_mantenimiento = escritorios.filter(estado='mantenimiento').count()
    
    tasa_ocupacion = (escritorios_ocupados / total_escritorios * 100) if total_escritorios > 0 else 0
    
    # Metros cuadrados totales
    total_metros = sum([sala.metros_cuadrados for sala in salas])
    
    # Reservas del mes actual
    reservas_mes = ReservaSala.objects.filter(
        fecha__month=date.today().month,
        fecha__year=date.today().year
    )
    
    context = {
        'total_escritorios': total_escritorios,
        'escritorios_ocupados': escritorios_ocupados,
        'escritorios_disponibles': escritorios_disponibles,
        'escritorios_mantenimiento': escritorios_mantenimiento,
        'tasa_ocupacion': round(tasa_ocupacion, 2),
        'total_metros': total_metros,
        'total_salas': salas.count(),
        'reservas_mes': reservas_mes.count(),
    }
    return render(request, 'reportes/ocupacion.html', context)


# ==================== CRUD ESCRITORIOS DEDICADOS ====================

@login_required
def escritorio_lista(request):
    escritorios = EscritorioDedicado.objects.all()
    return render(request, 'escritorios/listado.html', {'escritorios': escritorios})


@login_required
def escritorio_mapa(request):
    # Vista del mapa interactivo con jQuery UI Draggable
    escritorios = EscritorioDedicado.objects.all().order_by('piso', 'codigo')
    pisos = escritorios.values_list('piso', flat=True).distinct()
    return render(request, 'escritorios/mapa.html', {'escritorios': escritorios, 'pisos': pisos})


# ==================== CRUD RESERVAS DE SALAS ====================

@login_required
def reserva_lista(request):
    if request.user.is_superuser:
        reservas = ReservaSala.objects.all().order_by('-fecha', '-hora_inicio')
    else:
        # Usuario normal ve solo sus reservas
        try:
            miembro = Miembro.objects.get(usuario=request.user)
            reservas = ReservaSala.objects.filter(miembro=miembro).order_by('-fecha', '-hora_inicio')
        except Miembro.DoesNotExist:
            reservas = []
    return render(request, 'reservas/listado.html', {'reservas': reservas})


@login_required
def reserva_calendario(request):
    # Vista con FullCalendar
    salas = SalaReunion.objects.filter(activo=True)
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'reservas/calendario.html', {'salas': salas, 'miembros': miembros})


@login_required
def reservas_api(request):
    # API para FullCalendar - retorna JSON con las reservas
    reservas = ReservaSala.objects.all()
    eventos = []
    for reserva in reservas:
        eventos.append({
            'id': reserva.id,
            'title': f"{reserva.sala.nombre} - {reserva.miembro.nombre}",
            'start': f"{reserva.fecha}T{reserva.hora_inicio}",
            'end': f"{reserva.fecha}T{reserva.hora_fin}",
            'backgroundColor': '#0d6efd' if reserva.estado == 'confirmada' else '#6c757d',
            'borderColor': '#0d6efd' if reserva.estado == 'confirmada' else '#6c757d',
        })
    return JsonResponse(eventos, safe=False)


@login_required
def nueva_reserva(request):
    salas = SalaReunion.objects.filter(activo=True)
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'reservas/nuevo.html', {'salas': salas, 'miembros': miembros})



@login_required
def editar_reserva(request, id):
    reserva = get_object_or_404(ReservaSala, id=id)
    salas = SalaReunion.objects.filter(activo=True)
    miembros = Miembro.objects.filter(activo=True)
    return render(request, 'reservas/editar.html', {'reserva': reserva, 'salas': salas, 'miembros': miembros})


@login_required
def procesar_edicion_reserva(request):
    if request.method == 'POST':
        reserva = get_object_or_404(ReservaSala, id=request.POST['id'])
        reserva.sala = get_object_or_404(SalaReunion, id=request.POST['sala'])
        reserva.miembro = get_object_or_404(Miembro, id=request.POST['miembro'])
        reserva.fecha = request.POST['fecha']
        
        hora_inicio = datetime.strptime(request.POST['hora_inicio'], '%H:%M').time()
        hora_fin = datetime.strptime(request.POST['hora_fin'], '%H:%M').time()
        reserva.hora_inicio = hora_inicio
        reserva.hora_fin = hora_fin
        
        # Recalcular costo
        horas = (datetime.combine(date.today(), hora_fin) - datetime.combine(date.today(), hora_inicio)).seconds / 3600
        reserva.costo_total = Decimal(horas) * reserva.sala.precio_hora
        
        reserva.proposito = request.POST['proposito']
        reserva.numero_asistentes = request.POST['numero_asistentes']
        reserva.estado = request.POST['estado']
        
        reserva.save()
        messages.success(request, 'Reserva actualizada correctamente.')
        return redirect('reserva_lista')


@login_required
def eliminar_reserva(request, id):
    reserva = get_object_or_404(ReservaSala, id=id)
    reserva.delete()
    messages.success(request, 'Reserva eliminada correctamente.')
    return redirect('reserva_lista')


# ==================== CRUD FACTURAS ====================

@login_required
def factura_lista(request):
    if request.user.is_superuser:
        facturas = Factura.objects.all().order_by('-fecha_emision')
    else:
        facturas = []
    return render(request, 'facturas/listado.html', {'facturas': facturas})


@login_required
def nueva_factura(request):
    empresas = EmpresaCliente.objects.filter(activo=True)
    return render(request, 'facturas/nuevo.html', {'empresas': empresas})


@login_required
@login_required
def guardar_factura(request):
    if request.method == 'POST':
        empresa = get_object_or_404(EmpresaCliente, id=request.POST['empresa'])
        subtotal = Decimal(request.POST['subtotal'])
        iva = subtotal * Decimal('0.15')  # 15% IVA
        total = subtotal + iva
        
        factura = Factura.objects.create(
            empresa=empresa,
            fecha_vencimiento=request.POST['fecha_vencimiento'],
            subtotal=subtotal,
            iva=iva,
            total=total,
            tipo_factura=request.POST['tipo_factura'],
            estado=request.POST.get('estado', 'pendiente'),
            notas=request.POST.get('notas', ''),
            pdf=request.FILES.get('pdf')
        )
        
        # Enviar email de notificación de factura
        try:
            fecha_ven = datetime.strptime(request.POST['fecha_vencimiento'], '%Y-%m-%d').strftime("%d/%m/%Y")
            asunto = f'Nueva Factura #{factura.numero_factura} - CoworkSpace KC'
            mensaje = f'''
Estimado/a {empresa.nombre},

Se ha generado una nueva factura:

📄 Número: {factura.numero_factura}
📅 Fecha Emisión: {factura.fecha_emision.strftime("%d/%m/%Y")}
📅 Fecha Vencimiento: {fecha_ven}
💵 Subtotal: ${subtotal}
💵 IVA (15%): ${iva}
💵 TOTAL: ${total}
📋 Tipo: {factura.get_tipo_factura_display()}
🔖 Estado: {factura.get_estado_display()}

{f"Notas: {factura.notas}" if factura.notas else ""}

Por favor, realiza el pago antes de la fecha de vencimiento.

Gracias por confiar en CoworkSpace KC.

Saludos,
Equipo CoworkSpace KC
            '''
            send_mail(
                asunto,
                mensaje,
                settings.DEFAULT_FROM_EMAIL,
                [empresa.email],
                fail_silently=True,
            )
        except Exception as e:
            print(f"Error enviando email: {e}")
        
        messages.success(request, 'Factura guardada correctamente. Se ha enviado un email a la empresa.')
        return redirect('factura_lista')


@login_required
def editar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    empresas = EmpresaCliente.objects.filter(activo=True)
    return render(request, 'facturas/editar.html', {'factura': factura, 'empresas': empresas})


@login_required
def procesar_edicion_factura(request):
    if request.method == 'POST':
        factura = get_object_or_404(Factura, id=request.POST['id'])
        factura.empresa = get_object_or_404(EmpresaCliente, id=request.POST['empresa'])
        factura.fecha_vencimiento = request.POST['fecha_vencimiento']
        
        subtotal = Decimal(request.POST['subtotal'])
        factura.subtotal = subtotal
        factura.iva = subtotal * Decimal('0.15')
        factura.total = factura.subtotal + factura.iva
        
        factura.tipo_factura = request.POST['tipo_factura']
        factura.estado = request.POST['estado']
        factura.notas = request.POST.get('notas', '')
        
        nuevo_pdf = request.FILES.get('pdf')
        if nuevo_pdf:
            if factura.pdf and os.path.isfile(factura.pdf.path):
                os.remove(factura.pdf.path)
            factura.pdf = nuevo_pdf
        
        factura.save()
        messages.success(request, 'Factura actualizada correctamente.')
        return redirect('factura_lista')


@login_required
def eliminar_factura(request, id):
    factura = get_object_or_404(Factura, id=id)
    if factura.pdf and os.path.isfile(factura.pdf.path):
        os.remove(factura.pdf.path)
    factura.delete()
    messages.success(request, 'Factura eliminada correctamente.')
    return redirect('factura_lista')


@login_required
def generar_pdf_factura(request, id):
    # Generar PDF de la factura
    factura = get_object_or_404(Factura, id=id)
    # Aquí iría la lógica para generar PDF con reportlab
    # Por ahora solo retornamos un mensaje
    messages.info(request, 'Función de generación de PDF en desarrollo.')
    return redirect('factura_lista')


# ==================== REPORTES ====================

@login_required
def reportes(request):
    if not request.user.is_superuser:
        return redirect('inicio')
    
    # Estadísticas para la página principal de reportes
    total_empresas = EmpresaCliente.objects.filter(activo=True).count()
    total_miembros = Miembro.objects.filter(activo=True).count()
    total_salas = SalaReunion.objects.filter(activo=True).count()
    total_reservas = ReservaSala.objects.filter(
        fecha__month=date.today().month,
        fecha__year=date.today().year
    ).count()
    
    context = {
        'total_empresas': total_empresas,
        'total_miembros': total_miembros,
        'total_salas': total_salas,
        'total_reservas': total_reservas,
    }
    return render(request, 'reportes/index.html', context)


@login_required
def reporte_ocupacion(request):
    if not request.user.is_superuser:
        return redirect('inicio')
    
    # Reporte de tasa de ocupación por metros cuadrados
    salas = SalaReunion.objects.filter(activo=True)
    escritorios = EscritorioDedicado.objects.all()
    
    total_escritorios = escritorios.count()
    escritorios_ocupados = escritorios.filter(estado='ocupado').count()
    escritorios_disponibles = escritorios.filter(estado='disponible').count()
    escritorios_mantenimiento = escritorios.filter(estado='mantenimiento').count()
    
    tasa_ocupacion = (escritorios_ocupados / total_escritorios * 100) if total_escritorios > 0 else 0
    
    # Metros cuadrados totales
    total_metros = sum([sala.metros_cuadrados for sala in salas])
    
    context = {
        'salas': salas,
        'total_escritorios': total_escritorios,
        'escritorios_ocupados': escritorios_ocupados,
        'escritorios_disponibles': escritorios_disponibles,
        'escritorios_mantenimiento': escritorios_mantenimiento,
        'tasa_ocupacion': round(tasa_ocupacion, 2),
        'total_metros': total_metros,
    }
    return render(request, 'reportes/ocupacion.html', context)


@login_required
def reporte_facturacion(request):
    if not request.user.is_superuser:
        return redirect('inicio')
    
    # Reporte de facturación por empresa
    empresas = EmpresaCliente.objects.filter(activo=True)
    datos_empresas = []
    
    total_facturacion = Decimal('0.00')
    
    for empresa in empresas:
        facturas = Factura.objects.filter(empresa=empresa)
        facturas_pagadas = facturas.filter(estado='pagada')
        facturas_pendientes = facturas.filter(estado='pendiente')
        
        total_empresa = sum([f.total for f in facturas_pagadas])
        pendiente_empresa = sum([f.total for f in facturas_pendientes])
        
        # Consumo de horas de salas
        reservas = ReservaSala.objects.filter(miembro__empresa=empresa, estado='completada')
        total_horas = Decimal('0.00')
        for reserva in reservas:
            horas = (datetime.combine(date.today(), reserva.hora_fin) - 
                    datetime.combine(date.today(), reserva.hora_inicio)).seconds / 3600
            total_horas += Decimal(horas)
        
        total_facturacion += total_empresa
        
        datos_empresas.append({
            'empresa': empresa,
            'total_pagado': total_empresa,
            'total_pendiente': pendiente_empresa,
            'horas_salas': round(total_horas, 2),
            'num_facturas': facturas.count(),
        })
    
    context = {
        'datos_empresas': datos_empresas,
        'total_facturacion': total_facturacion,
    }
    return render(request, 'reportes/facturacion.html', context)
