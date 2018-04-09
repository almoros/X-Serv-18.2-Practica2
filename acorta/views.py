from django.shortcuts import render
from django.http import HttpResponse
from acorta.models import Pages
from django.views.decorators.csrf import csrf_exempt
import urllib.parse

# Create your views here.

@csrf_exempt

# Cuestionario inicial en el que introducimos las URLs.
def main(request):
    reply = """
        <form action="" method="post">
          Introduce la URL a acortar:
          <input type="text" name="url" value="" />
          <br/>

          <input type="submit" value="Enviar" />
        </form>

        """
    Lista = Pages.objects.all() # Mostramos las URLs almacenadas.

# Cuando hacemos PUT o POST vamos a introducir una página web nueva.
    if request.method == "PUT" or request.method == "POST":
        body = str(request.body) # Recogemos el body que nos introducen.
        url = body.split('&')[0].split('=')[1][:-1]
        url = str(urllib.parse.unquote(url, 'utf-8', 'replace')) # Aseguramos decodificar la url.

# La función url.startswith() nos devuelve el comienzo de la URL, también podemos hacerlo como en la práctica 1.
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "http://" + url

# Comprobamos que no exista ya esa entrada.
        ready = False
        for contenido in Lista:
            if url in contenido.url:
                ready = True
        if not ready:
            guardar = Pages(url=url, page=len(Lista))
            guardar.save()

    Lista = Pages.objects.all() # Mostramos las URLs almacenadas.

# Volcamos la base de datos en Lista y la imprimimos
    reply += "<br/><img src='https://tucasaenaranjuez.com/wp-content/uploads/2016/11/separador.png'>"
    reply += "<h1><li type='circle'>Listado de URLs guardados:</h1></li>"

    reply += "<ul>"
    for contenido in Lista:
        reply += "<li><p>" + '<a href="' + contenido.url + '">' + contenido.url + "<a/>: La ID asignada es " + str(contenido.page)
    reply += "</ul>"

    return HttpResponse(reply)

# Esta función nos permite buscar la URL guardada a través de su id corto.
def recurso(request, num):

    Lista = Pages.objects.all() # Mostramos las URLs almacenadas.
    try:
        url = Lista[int(num)].url
        reply = ('<html><head><meta http-equiv="Refresh" content="5;url='+ url +'"></head>' \
        + "<body><h1><p style='color:blue;'>Redirigiendo en 5 segundos...</p>" + "<img src='https://blog.hostalia.com/wp-content/themes/hostalia/images/redirigir-dominio-blog-hostalia-hosting.jpg'>" \
        + "</h1></body></html>")
    except:
        reply = '<head><meta http-equiv="Refresh" content="3;url=http://localhost:8000"></head><h1><p style="color:blue;">La página acortada no existe.</p></h1>'
    return HttpResponse(reply)

def error(request):

    return HttpResponse('<head><meta http-equiv="Refresh" content="5;url=http://localhost:8000"></head><h1><p style="color:red;">RECURSO INTRODUCIDO NO VÁLIDO</p>' + "<img src='https://reygif.com/media/mini-senal-stop-79483.gif'>" '</h1> Tiene que ser un numero.')
