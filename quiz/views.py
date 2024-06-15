from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from .models import Pregunta, Opcion, Resultado
from .forms import FormularioCuestionario, FormularioRegistro
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, 'Has iniciado sesión exitosamente.')
            return redirect('vista_cuestionario')
        else:
            messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def registro(request):
    if request.method == 'POST':
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            messages.success(request, 'Registro exitoso. Has iniciado sesión.')
            return redirect('iniciar_sesion')  # Redirige al inicio de sesión
        else:
            messages.error(request, 'Por favor corrige los errores a continuación.')
    else:
        form = FormularioRegistro()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def vista_cuestionario(request):
    preguntas = Pregunta.objects.all()
    if request.method == 'POST':
        form = FormularioCuestionario(request.POST, preguntas=preguntas)
        if form.is_valid():
            for pregunta in preguntas:
                seleccion = form.cleaned_data.get(f'pregunta_{pregunta.id}')
                if seleccion:
                    opcion = Opcion.objects.get(id=seleccion)
                    Resultado.objects.create(
                        usuario=request.user,
                        pregunta=pregunta,
                        opcion_seleccionada=opcion,
                        es_correcta=opcion.es_correcta
                    )
            messages.success(request, 'Cuestionario completado exitosamente.')
            return redirect('vista_resultados')
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        form = FormularioCuestionario(preguntas=preguntas)
    return render(request, 'quiz/cuestionario.html', {'form': form})

@login_required
def vista_resultados(request):
    resultados = Resultado.objects.filter(usuario=request.user)
    aciertos = resultados.filter(es_correcta=True).count()
    desaciertos = resultados.filter(es_correcta=False).count()
    return render(request, 'quiz/resultados.html', {
        'resultados': resultados,
        'aciertos': aciertos,
        'desaciertos': desaciertos
    })

@login_required
def generar_pdf(request):
    resultados = Resultado.objects.filter(usuario=request.user)
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="resultados.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    p.drawString(100, height - 100, "Resultados del Cuestionario")
    y = height - 120

    for resultado in resultados:
        text = f"{resultado.pregunta.texto} - {resultado.opcion_seleccionada.texto} - {'Correcto' if resultado.es_correcta else 'Incorrecto'}"
        p.drawString(100, y, text)
        y -= 20

    p.showPage()
    p.save()
    return response

def cerrar_sesion(request):
    logout(request)
    messages.success(request, 'Has cerrado sesión exitosamente.')
    return redirect('login')
