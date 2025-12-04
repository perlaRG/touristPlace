from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Usuarios
import urllib.parse
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q
from django.core.paginator import Paginator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

#Creado por perla
def registrar_datos(request):
    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm = request.POST.get('confirm_password', '')
        telefono = request.POST.get('telefono', '').strip()

        # Validación mínima en servidor
        if not (nombre and email and password and confirm and telefono):
            mensaje = urllib.parse.quote_plus('faltan campos obligatorios')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        # Validar formato de email
        try:
            validate_email(email)
        except ValidationError:
            mensaje = urllib.parse.quote_plus('formato de email inválido')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        if password != confirm:
            mensaje = urllib.parse.quote_plus('las contraseñas no coinciden')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        # Evitar emails duplicados
        if Usuarios.objects.filter(email=email).exists():
            mensaje = urllib.parse.quote_plus('email ya registrado')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        # Hashear la contraseña antes de guardar
        hashed = make_password(password)

        nuevo_registro = Usuarios(
            nombre=nombre,
            email=email,
            contraseña=hashed,
            telefono=telefono,
        )
        nuevo_registro.save()

        mensaje = urllib.parse.quote_plus('cuenta creada satisfactoriamente')
        return redirect(reverse('nucleo:iniciosesion') + f'?mensaje={mensaje}')

    return render(request, 'registro.html') 

# Vistas simples que renderizan las plantillas existentes.
def index(request):
	return render(request, 'index.html')


def ajustes(request):
	return render(request, 'ajustes.html')

def iniciosesion(request):
    mensaje = request.GET.get('mensaje')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if not email or not password:
            mensaje_err = urllib.parse.quote_plus('faltan campos obligatorios')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje_err}')

        try:
            usuario = Usuarios.objects.get(email=email)
        except Usuarios.DoesNotExist:
            mensaje_err = urllib.parse.quote_plus('credenciales inválidas')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje_err}')

        if check_password(password, usuario.contraseña):
            # Crear sesión mínima
            request.session['usuario_id'] = usuario.id
            request.session['usuario_nombre'] = usuario.nombre
            return redirect(reverse('nucleo:principal'))
        else:
            mensaje_err = urllib.parse.quote_plus('credenciales inválidas')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje_err}')

    return render(request, 'iniciosesion.html', {'mensaje': mensaje})


def pantallaPrincipal(request):
	return render(request, 'pantallaPrincipal.html')


def registro(request):
	return render(request, 'registro.html')


def advertencia(request):
	return render(request, 'advertencia.html')


def error_404(request):
	return render(request, '404.html')

#Creado por Hannah
def usuarios_list(request):
    q = request.GET.get('q', '').strip()
    qs = Usuarios.objects.all()
    if q:
        qs = qs.filter(
            Q(nombre__icontains=q) |
            Q(email__icontains=q) |
            Q(telefono__icontains=q)
        ).order_by('nombre')

    paginator = Paginator(qs, 10)  # 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'usuarios_list.html', {'usuarios': page_obj, 'q': q})

#Creado por Fernanda
def editar_usuario(request, id):
    try:
        usuario = Usuarios.objects.get(id=id)
    except Usuarios.DoesNotExist:
        mensaje = urllib.parse.quote_plus('usuario no encontrado')
        return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

    if request.method == 'POST':
        nombre = request.POST.get('nombre', '').strip()
        email = request.POST.get('email', '').strip().lower()
        telefono = request.POST.get('telefono', '').strip()
        nueva_contraseña = request.POST.get('password', '')

        # Validar campos no vacíos
        if not (nombre and email and telefono):
            mensaje = urllib.parse.quote_plus('faltan campos obligatorios')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        # Validar formato de email
        try:
            validate_email(email)
        except ValidationError:
            mensaje = urllib.parse.quote_plus('formato de email inválido')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        # Verificar si el email ya existe en otro usuario
        if email != usuario.email and Usuarios.objects.filter(email=email).exists():
            mensaje = urllib.parse.quote_plus('email ya registrado')
            return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

        # Actualizar datos
        usuario.nombre = nombre
        usuario.email = email
        usuario.telefono = telefono

        # Si se proporciona contraseña nueva, actualizarla
        if nueva_contraseña:
            usuario.contraseña = make_password(nueva_contraseña)

        usuario.save()

        mensaje = urllib.parse.quote_plus('usuario actualizado correctamente')
        return redirect(reverse('nucleo:usuarios_list') + f'?mensaje={mensaje}')

    return render(request, 'editar.html', {'usuario': usuario})


#Creado por Miguel
def eliminar_usuario(request, id):
    try:
        usuario = Usuarios.objects.get(id=id)
    except Usuarios.DoesNotExist:
        mensaje = urllib.parse.quote_plus('usuario no encontrado')
        return redirect(reverse('nucleo:advertencia') + f'?mensaje={mensaje}')

    if request.method == 'POST':
        nombre_usuario = usuario.nombre
        usuario.delete()
        mensaje = urllib.parse.quote_plus(f'usuario {nombre_usuario} eliminado correctamente')
        return redirect(reverse('nucleo:usuarios_list') + f'?mensaje={mensaje}')

    # GET: mostrar página de confirmación
    return render(request, 'confirmar_eliminar.html', {'usuario': usuario})