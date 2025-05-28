import cv2
import numpy as np
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from .forms import PropiedadForm
from django.shortcuts import render, redirect
from .models import Propiedad

def procesar_imagen(imagen):
    imagen.seek(0)
    file_bytes = np.asarray(bytearray(imagen.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
    img = cv2.resize(img, (800, 600))
    is_success, buffer = cv2.imencode(".jpg", img)
    io_buf = io.BytesIO(buffer)
    return InMemoryUploadedFile(io_buf, None, 'propiedad.jpg', 'image/jpeg', io_buf.getbuffer().nbytes, None)

def agregar_propiedad(request):
    if request.method == 'POST':
        form = PropiedadForm(request.POST, request.FILES)
        if form.is_valid():
            propiedad = form.save(commit=False)
            propiedad.propietario = request.user
            propiedad.imagen = procesar_imagen(request.FILES['imagen'])
            propiedad.save()
            return redirect('mis_propiedades')
    else:
        form = PropiedadForm()
    return render(request, 'agregar_propiedad.html', {'form': form})