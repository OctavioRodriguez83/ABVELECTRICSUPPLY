from django.http import JsonResponse
from django.core.files.storage import FileSystemStorage
import os
from django.conf import settings
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.template.context_processors import request
from django.template.loader import render_to_string
from django.utils import timezone
from django.db.models import Sum
from django.http import FileResponse, Http404, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.core.management import call_command
from django.urls import reverse
from django.core.paginator import Paginator

from .models import *
from .forms import *


# Create your views here.
#---------------------------------------------CRUD PRODUCTOS-------------------------------------------------------#
@login_required
def dashboard(request):
    total_products = Producto.objects.count()
    return render(request, 'adm/dashboard/dashboard.html', {
        'total_products': total_products,
    })

#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------CRUD MARCAS----------------------------------------------------------#                                  
@login_required
def marcas(request):
    filtro = request.GET.get('status', 'active')
    if filtro == 'inactive':
        marcas = Marca.objects.filter(status=False)
    else:
        marcas = Marca.objects.filter(status=True)

    if request.method == "POST":
        formM = MarcaForm(request.POST, request.FILES)
        if formM.is_valid():
            formM.save()
            return HttpResponseRedirect(reverse('marcas'))
        else:
            print(formM.errors)
    else:
        formM = MarcaForm()

    return render(request, 'adm/marcas/marcas.html', {'marcas': marcas, 'formM': formM, 'filtro': filtro})

@login_required
def eliminar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    marca.status = False  
    marca.save()
    return HttpResponseRedirect(reverse('marcas'))

@login_required
def editar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    marcas = Marca.objects.filter(status=True)

    if request.method == "POST":
        marca.marca_name = request.POST.get('marca_name')
        marca.marca_descripcion = request.POST.get('marca_descripcion')

        if 'marca_url_img' in request.FILES:
            marca.marca_url_img = request.FILES['marca_url_img']

        marca.save()
        return HttpResponseRedirect(reverse('marcas'))

    formM = MarcaForm()
    return render(request, 'adm/marcas/editar_marcas.html', {
        'marca': marca,
        'marcas': marcas,
        'formM': formM
    })

@login_required
def restaurar_marca(request, marca_id):
    marca = get_object_or_404(Marca, id=marca_id)
    marca.status = True
    marca.save()
    return HttpResponseRedirect(reverse('marcas'))
#------------------------------------------------------------------------------------------------------------------#

#------------------------------------------CRUD CATEGORIAS---------------------------------------------------------#


@login_required
def categorias(request):
    filtro = request.GET.get('status', 'active')
    if filtro == 'inactive':
        categorias = Categoria.objects.filter(statusCategoria=False)
    else:
        categorias = Categoria.objects.filter(statusCategoria=True)

    if request.method == "POST":
        formC = CategoriaForm(request.POST, request.FILES)
        if formC.is_valid():
            formC.save()
            return HttpResponseRedirect(reverse('categorias'))
        else:
            print(formC.errors)
    else:
        formC = CategoriaForm()

    return render(request, 'adm/categorias/categorias.html', {'categorias': categorias, 'formC': formC, 'filtro': filtro})


@login_required
def editar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categorias = Categoria.objects.filter(statusCategoria=True)  # Categorías activas

    if request.method == "POST":
        categoria.categoria_name = request.POST.get('categoria_name')
        categoria.categoria_descripcion = request.POST.get('categoria_descripcion')

        if 'categoria_url_img' in request.FILES:
            categoria.categoria_url_img = request.FILES['categoria_url_img']

        # Actualiza el estado activo/inactivo mediante checkbox
        status = request.POST.get('statusCategoria')
        categoria.statusCategoria = True if status == 'on' else False

        categoria.save()
        return HttpResponseRedirect(reverse('categorias'))

    formC = CategoriaForm()
    return render(request, 'adm/categorias/editar_categorias.html', {
        'categoria': categoria,
        'categorias': categorias,
        'formC': formC
    })

@login_required
def eliminar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.statusCategoria = False
    categoria.save()
    return HttpResponseRedirect(reverse('categorias'))


@login_required
def restaurar_categoria(request, categoria_id):
    categoria = get_object_or_404(Categoria, id=categoria_id)
    categoria.statusCategoria = True
    categoria.save()
    return HttpResponseRedirect(reverse('categorias'))

#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------CRUD CARROUSEL BANNER-----------------------------------------------#

@login_required
def carrouselBanner(request):
    posts = CarrouselBanner.objects.filter(statusBanner=True)
    if request.method == "POST":
        formp = CarrouselBannerForm(request.POST, request.FILES)
        if formp.is_valid():
            formp.save()
            return HttpResponseRedirect(reverse('carrouselBanner'))
        else:
            print(formp.errors)
    formp = CarrouselBannerForm()
    return render(request, 'adm/carrouselBanner/carrouselBanner.html', {'posts': posts, 'formp': formp} )

@login_required
def editar_carrouselBanner(request, carrouselBanner_id):
    formp = CarrouselBannerForm()
    posts = CarrouselBanner.objects.filter(statusBanner=True)
    carrouselBanner = get_object_or_404(CarrouselBanner, id=carrouselBanner_id)

    if request.method == "POST":
        carrouselBanner.carrouselBanner_name = request.POST.get('carrouselBanner_name')
        carrouselBanner.carrouselBanner_descripcion = request.POST.get('carrouselBanner_descripcion')

        if 'carrouselBanner_url_img' in request.FILES:
            carrouselBanner.carrouselBanner_url_img = request.FILES['carrouselBanner_url_img']

        carrouselBanner.save()
        return HttpResponseRedirect(reverse('carrouselBanner'))

    return render(request, 'adm/carrouselBanner/editar_carrouselBanner.html', {'posts': posts,'carrouselBanner': carrouselBanner,'formp': formp})

@login_required
def eliminar_carrouselBanner(request, carrouselBanner_id):
    carrouselBanner = get_object_or_404(CarrouselBanner, id=carrouselBanner_id)
    carrouselBanner.statusBanner = False
    carrouselBanner.save()
    return HttpResponseRedirect(reverse('carrouselBanner'))
#------------------------------------------------------------------------------------------------------------------#

#-----------------------------------------VISTAS LOGIN-------------------------------------------------------------#
def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')  
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)  # Buscar usuario por email
        except User.DoesNotExist:
            user = None
        
        if user is not None:
            user = authenticate(request, username=user.username, password=password)  # Autenticar con username
            if user is not None:
                auth_login(request, user)
                return redirect('dashboard')
        
        error_message = 'Correo o contraseña incorrectos'
        return render(request, 'adm/login/login.html', {'error': error_message})

    return render(request, 'adm/login/login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')
#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------VISTAS USUARIOS-------------------------------------------------------#

@login_required
def usuarios(request):
    usuarios = User.objects.all()
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pwd = form.cleaned_data.get('password')
            if pwd:
                user.set_password(pwd)
            else:
                user.set_unusable_password()
            user.save()
            return redirect(reverse('usuarios'))
    else:
        form = UsuarioForm()
    return render(request, 'adm/usuarios/usuarios.html', {'usuarios': usuarios, 'form': form})

# python
@login_required
def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        data = request.POST

        nuevo_username = data.get('username')
        if nuevo_username:
            usuario.username = nuevo_username

        nuevo_first_name = data.get('first_name')
        if nuevo_first_name:
            usuario.first_name = nuevo_first_name

        nuevo_last_name = data.get('last_name')
        if nuevo_last_name:
            usuario.last_name = nuevo_last_name

        nuevo_email = data.get('email')
        if nuevo_email:
            usuario.email = nuevo_email

        # Actualiza la contraseña solo si se pasa y cumple con la longitud mínima (8 caracteres)
        nuevo_password = data.get('password', '')
        if nuevo_password and len(nuevo_password) >= 8:
            usuario.set_password(nuevo_password)
        # Sino no se modifica la contraseña

        usuario.is_superuser = True if data.get('is_superuser') == 'on' else False

        usuario.is_active = True if data.get('is_active') == 'on' else False

        usuario.save()
        return redirect(reverse('usuarios'))

    return render(request, 'adm/usuarios/usuarios.html', {
        'usuarios': usuarios,
        'usuario_actual': usuario,
    })

@login_required
def eliminar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    usuario.delete()
    return redirect(reverse('usuarios'))
    

#------------------------------------------------------------------------------------------------------------------#

#------------------------------------------------CRUD DE TIENDAS---------------------------------------------------#

@login_required
def tiendas(request):
    # Traemos todas las tiendas
    tiendas = Tienda.objects.all()

    if request.method == "POST":
        formT = TiendaForm(request.POST, request.FILES)
        if formT.is_valid():
            formT.save()
            return redirect(reverse('tiendas'))
        else:
            print(formT.errors)
    else:
        formT = TiendaForm()

    return render(request, 'adm/tiendas/tiendas.html', {
        'tiendas': tiendas,
        'formT': formT
    })

@login_required
def editar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    tiendas = Tienda.objects.all()

    if request.method == "POST":
        # Vinculamos el formulario a la instancia para editar
        formT = TiendaForm(request.POST, request.FILES, instance=tienda)
        if formT.is_valid():
            formT.save()
            return redirect(reverse('tiendas'))
        else:
            print(formT.errors)
    else:
        # Inicializamos con los datos actuales de la tienda
        formT = TiendaForm(instance=tienda)

    return render(request, 'adm/tiendas/editar_tienda.html', {
        'tiendas': tiendas,
        'tienda': tienda,
        'formT': formT
    })

@login_required
def eliminar_tienda(request, tienda_id):
    tienda = get_object_or_404(Tienda, id=tienda_id)
    tienda.delete()  # eliminas la tienda
    return redirect(reverse('tiendas'))
#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------CRUD DE EMPRESAS-----------------------------------------------------#
@login_required
def empresas(request):
    empresas = Empresa.objects.all()
    if request.method == "POST":
        formE = EmpresaForm(request.POST, request.FILES)
        if formE.is_valid():
            formE.save()
            return redirect(reverse('empresas'))
        else:
            print(formE.errors)
    else:
        formE = EmpresaForm()

    return render(request, 'adm/empresas/empresas.html', {
        'empresas': empresas,
        'formE': formE
    })

@login_required
def editar_empresa(request, empresa_id):
    empresas = Empresa.objects.all()
    empresa = get_object_or_404(Empresa, id=empresa_id)
    formE = EmpresaForm()
    if request.method == "POST":
        empresa.empresa_nombre = request.POST.get("empresa_nombre")
        empresa.empresa_descripcion = request.POST.get("empresa_descripcion")
        if "empresa_logo" in request.FILES:
            empresa.empresa_logo = request.FILES["empresa_logo"]
        empresa.save()
        return redirect(reverse("empresas"))
    return render(request, "adm/empresas/editar_empresa.html", {"empresas": empresas, "empresa": empresa, "formE": formE})

@login_required
def eliminar_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    empresa.delete()
    return redirect(reverse("empresas"))

#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------VISTAS ALMACEN-------------------------------------------------------#

@login_required
def almacenes(request):
    almacenes_list = Almacen.objects.all()
    if request.method == "POST":
        formA = AlmacenForm(request.POST)
        if formA.is_valid():
            formA.save()
            return redirect(reverse('almacenes'))
        else:
            print(formA.errors)
    else:
        formA = AlmacenForm()
    return render(request, 'adm/almacenes/almacenes.html', {'almacenes': almacenes_list, 'formA': formA})

def editar_almacen(request, almacen_id):
    almacenes_list = Almacen.objects.all()
    almacen = get_object_or_404(Almacen, id=almacen_id)
    empresas_list = Empresa.objects.all()
    if request.method == "POST":
        formA = AlmacenForm(request.POST, instance=almacen)
        if formA.is_valid():
            formA.save()
            return redirect(reverse("almacenes"))
    else:
        formA = AlmacenForm(instance=almacen)
    return render(request, 'adm/almacenes/editar_almacen.html', {
        'almacenes': almacenes_list,
        'almacen': almacen,
        'formA': formA,
        'empresas': empresas_list
    })

@login_required
def eliminar_almacen(request, almacen_id):
    almacen = get_object_or_404(Almacen, id=almacen_id)
    almacen.delete()
    return redirect(reverse("almacenes"))

#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------VISTAS PRODUCTOS-----------------------------------------------------#

@login_required
def productos(request):
    # Suma el stock de cada producto según sus inventarios
    productos_list = Producto.objects.all().annotate(total_stock=Sum('inventario__stock'))
    return render(
        request,
        "adm/productos/productos.html",
        {"productos": productos_list}
    )

@login_required
def ver_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    inventarios = Inventario.objects.filter(producto=producto)
    imagenes_secundarias = ImagenSecundariaProducto.objects.filter(producto=producto)
    form = InventarioForm()
    # Calcula la suma total de stock
    total_stock = inventarios.aggregate(total=Sum('stock')).get('total') or 0
    return render(
        request,
        "adm/productos/producto.html",
        {
            "producto": producto,
            "inventarios": inventarios,
            "imagenes_secundarias": imagenes_secundarias,
            "form": form,
            "total_stock": total_stock,
        }
    )

@login_required
def crear_producto(request):
    # Se encarga únicamente de la creación
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect(reverse("productos"))
    else:
        form = ProductoForm()

    marcas = Marca.objects.all()
    categorias = Categoria.objects.all()
    return render(request, "adm/productos/crear_producto.html", {"form": form, "marcas": marcas, "categorias": categorias})


@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES, instance=producto)
        if form.is_valid():
            form.save()
            return redirect(reverse("productos"))
        else:
            print(form.errors)
    else:
        form = ProductoForm(instance=producto)
    return render(request, "adm/productos/editar_producto.html", {"form": form, "producto": producto})

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    producto.delete()
    return redirect(reverse("productos"))

#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------VISTAS SERVICIOS-----------------------------------------------------#

@login_required
def servicios(request):
    servicios_list = Servicio.objects.all()
    if request.method == "POST":
        formServ = ServicioForm(request.POST, request.FILES)
        if formServ.is_valid():
            formServ.save()
            return redirect(reverse("servicios"))
        else:
            print(formServ.errors)
    else:
        formServ = ServicioForm()
    return render(request, "adm/servicios/servicios.html", {"servicios": servicios_list, "formServ": formServ})

@login_required
def editar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    if request.method == "POST":
        formServ = ServicioForm(request.POST, request.FILES, instance=servicio)
        if formServ.is_valid():
            formServ.save()
            return redirect(reverse("servicios"))
        else:
            print(formServ.errors)
    else:
        formServ = ServicioForm(instance=servicio)
    return render(request, "adm/servicios/editar_servicio.html", {"servicio": servicio, "formServ": formServ})

@login_required
def eliminar_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, id=servicio_id)
    servicio.delete()
    return redirect(reverse("servicios"))

#------------------------------------------------------------------------------------------------------------------#

#---------------------------------------------VISTAS PROYECTOS-----------------------------------------------------#

@login_required
def proyectos(request):
    proyectos_list = Proyecto.objects.all()
    if request.method == "POST":
        formProj = ProyectoForm(request.POST, request.FILES)
        if formProj.is_valid():
            formProj.save()
            return redirect(reverse("proyectos"))
        else:
            print(formProj.errors)
    else:
        formProj = ProyectoForm()
    return render(request, "adm/proyectos/proyectos.html", {"proyectos": proyectos_list, "formProj": formProj})

@login_required
def editar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyectos_list = Proyecto.objects.all()
    if request.method == "POST":
        formProj = ProyectoForm(request.POST, request.FILES, instance=proyecto)
        if formProj.is_valid():
            formProj.save()
            return redirect(reverse("proyectos"))
        else:
            print(formProj.errors)
    else:
        formProj = ProyectoForm(instance=proyecto)
    return render(request, "adm/proyectos/editar_proyecto.html", {"proyecto": proyecto, "formProj": formProj})

@login_required
def eliminar_proyecto(request, proyecto_id):
    proyecto = get_object_or_404(Proyecto, id=proyecto_id)
    proyecto.delete()
    return redirect(reverse("proyectos"))

#------------------------------------------------------------------------------------------------------------------#

#--------------------------------------------VISTAS PRODUCTOS DESTACADOS-------------------------------------------#


@login_required
def productos_destacados(request):
    destacados = ProductoDestacado.objects.select_related(
        'producto',
        'producto__categoria',
        'producto__marca'
    ).all()
    return render(request, "adm/productos_destacados/productos_destacados.html", {
        'destacados': destacados,
    })

@login_required
def agregar_destacado(request):
    if request.method == "POST":
        # Obtiene lista de IDs enviados
        selected_ids = request.POST.getlist('productos')

        # Solo agrega los nuevos productos destacados, sin eliminar los existentes
        for pid in selected_ids:
            try:
                prod = Producto.objects.get(pk=pid)
                # Solo crea si no existe ya como destacado
                ProductoDestacado.objects.get_or_create(producto=prod)
            except Producto.DoesNotExist:
                continue

        # Redirige a la lista de destacados
        return redirect('productos_destacados')

    # GET: envía todos los productos para la tabla
    productos = Producto.objects.all()
    return render(request,
                  "adm/productos_destacados/agregar_destacado.html",
                  {"productos": productos})

@login_required
def eliminar_destacado(request, destacado_id):
    destacado = get_object_or_404(ProductoDestacado, id=destacado_id)
    destacado.delete()
    return redirect('productos_destacados')


#------------------------------------------------------------------------------------------------------------------#

#-------------------------------------------------VISTAS INVENTARIO------------------------------------------------#

@login_required
def agregar_inventario(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == "POST":
        form = InventarioForm(request.POST)
        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.producto = producto
            inventario.fecha_modificacion = None  # Sin modificaciones aún
            inventario.save()
            return redirect(reverse("ver_producto", args=[producto_id]))
    else:
        form = InventarioForm()

    # Se recolectan datos adicionales para el render en caso de error o GET
    inventarios = Inventario.objects.filter(producto=producto)
    imagenes_secundarias = ImagenSecundariaProducto.objects.filter(producto=producto)

    return render(
        request,
        "adm/productos/producto.html",
        {
            "producto": producto,
            "inventarios": inventarios,
            "imagenes_secundarias": imagenes_secundarias,
            "form": form,
        }
    )

@login_required
def modificar_stock(request, inventario_id):
    inventario = get_object_or_404(Inventario, id=inventario_id)
    producto = inventario.producto
    if request.method == "POST":
        form = InventarioForm(request.POST, instance=inventario)
        form.fields.pop("almacen", None)  # elimina el campo que no se envía
        if form.is_valid():
            inventario = form.save(commit=False)
            inventario.fecha_modificacion = timezone.now()
            inventario.save()
            return redirect(reverse("ver_producto", args=[producto.id]))
    else:
        form = InventarioForm(instance=inventario)
        form.fields.pop("almacen", None)

    inventarios = Inventario.objects.filter(producto=producto)
    imagenes_secundarias = ImagenSecundariaProducto.objects.filter(producto=producto)

    return render(
        request,
        "adm/productos/producto.html",
        {
            "producto": producto,
            "inventarios": inventarios,
            "imagenes_secundarias": imagenes_secundarias,
            "form": InventarioForm(),
            "form_modificar": form,
            "inventario_modificar": inventario,
        }
    )


#------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------VISTAS PLANTILLAS----------------------------------------------------#

@login_required
def plantillas(request):
    # Ruta donde se almacenan las plantillas
    templates_dir = os.path.join(settings.BASE_DIR, 'files', 'Plantillas')
    available_templates = []

    # Detectar automáticamente las plantillas disponibles
    for file_name in os.listdir(templates_dir):
        if file_name.startswith('plantilla_') and file_name.endswith('.xlsx'):
            template_slug = file_name.replace('plantilla_', '').replace('.xlsx', '')
            available_templates.append({
                'name': template_slug.replace('_', ' ').capitalize(),
                'template_slug': template_slug
            })

    return render(request, 'adm/plantillas/plantillas.html', {'available_templates': available_templates})

@login_required
def download_template(request, template_slug):
    # Ruta donde se almacenan las plantillas
    templates_dir = os.path.join(settings.BASE_DIR, 'files', 'Plantillas')
    file_name = f'plantilla_{template_slug}.xlsx'
    file_path = os.path.join(templates_dir, file_name)

    if os.path.exists(file_path):
        return FileResponse(open(file_path, 'rb'), as_attachment=True)
    raise Http404("Plantilla no encontrada")

#------------------------------------------------------------------------------------------------------------------#
#----------------------------------------------VISTAS CARGA M------------------------------------------------------#
@login_required
def dashboard_carga(request):
    return render(request, 'adm/carga_masiva/dashboard_carga.html')


@login_required
def import_excel(request, model_slug):
    if request.method == 'POST':
        file = request.FILES.get('import_file')
        if not file:
            return JsonResponse({"status": "error", "message": "No se proporcionó un archivo"}, status=400)

        import_path = os.path.join(settings.MEDIA_ROOT, f'temp_{model_slug}.xlsx')
        with open(import_path, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)

        output_capture = OutputCapture()
        try:
            call_command(f'import_{model_slug}', path=import_path, stdout=output_capture)
        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)}, status=500)

        return JsonResponse({"status": "success", "messages": output_capture.get_messages()})

    return JsonResponse({"status": "error", "message": "Método no permitido"}, status=405)

class OutputCapture:
    def __init__(self):
        self.messages = []

    def write(self, message):
        if message.strip():  # Evita capturar líneas vacías
            self.messages.append(message.strip())

    def get_messages(self):
        return self.messages

@require_POST
def upload_images(request):
    model_slug = request.POST.get('model_slug')
    folder_map = {
        'empresas':  'Imagenes_Empresa',
        'almacenes': 'Imagenes_Almacen',
        'categorias':'Imagenes_Categoria',
        'marcas':    'Imagenes_Marca',
        'productos': 'Imagenes_Producto',
        'tiendas':   'Imagenes_Tienda',
    }
    if model_slug not in folder_map:
        return JsonResponse({'status': 'error', 'message': 'Modelo no válido.'}, status=400)

    # Se ajusta la ruta destino para guardar directamente en MEDIA_ROOT/<subcarpeta>
    subcarpeta = folder_map[model_slug]
    target_dir = os.path.join(settings.MEDIA_ROOT, subcarpeta)
    os.makedirs(target_dir, exist_ok=True)

    archivos = request.FILES.getlist('images')
    if not archivos:
        return JsonResponse({'status': 'error', 'message': 'No se seleccionaron archivos.'}, status=400)

    fs = FileSystemStorage(location=target_dir)
    saved_files = []
    for archivo in archivos:
        filename = fs.save(archivo.name, archivo)
        saved_files.append(filename)

    return JsonResponse({
        'status': 'success',
        'message': f'Se subieron {len(archivos)} imagen(es) a {subcarpeta}.',
        'files': saved_files
    })

#------------------------------------------------------------------------------------------------------------------#
#---------------------------------------VISTAS PROYECTOS DESTACADOS------------------------------------------------#

@login_required
def proyectos_destacados(request):
    destacados = ProyectoDestacado.objects.select_related(
        'proyecto'
    ).all()
    return render(request, 'adm/proyectos_destacados/proyectos_destacados.html', {
        'destacados': destacados,
    })

@login_required
def agregar_proyecto_destacado(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist('proyectos')
        for pid in selected_ids:
            try:
                proyecto = Proyecto.objects.get(id=pid)
                ProyectoDestacado.objects.get_or_create(proyecto=proyecto)
            except Proyecto.DoesNotExist:
                continue
        return redirect('proyectos_destacados')
    # Excluir proyectos ya destacados
    destacados_ids = ProyectoDestacado.objects.values_list('proyecto_id', flat=True)
    proyectos = Proyecto.objects.exclude(id__in=destacados_ids)
    return render(request, 'adm/proyectos_destacados/agregar_proyecto_destacado.html', {
        'proyectos': proyectos
    })

@login_required
def eliminar_proyecto_destacado(request, destacado_id):
    destacado = get_object_or_404(ProyectoDestacado, id=destacado_id)
    destacado.delete()
    return redirect('proyectos_destacados')

#------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------VISTAS PUBLICO-------------------------------------------------------#

def home(request):
    posts = CarrouselBanner.objects.filter(statusBanner=True)
    categorias = Categoria.objects.all()
    marcas = Marca.objects.filter(status=True)
    servicios = Servicio.objects.all()
    destacados = ProductoDestacado.objects.select_related('producto').all()

    # --- Cálculo de rangos para indicadores de carrusel ---
    # Carrusel Principal (#carouselExampleCaptions1)
    # Incluye el slide estático inicial + posts + categorías
    indicators_range_carrusel1 = range(1 + len(posts) + len(categorias))

    # Carrusel Superior Secundario (#carouselExampleCaptions2 - en #carruS)
    # Incluye el slide estático inicial + destacados
    indicators_range_carrusel2 = range(1 + len(destacados))

    # Carrusel Inferior Secundario (#carouselExampleCaptions3 - en #carruI)
    # Incluye el slide estático inicial + marcas
    indicators_range_carrusel3 = range(1 + len(marcas))
    # --- Fin del cálculo de rangos ---

    return render(request, 'publico/home/home.html', {
        'posts': posts,
        'marcas': marcas,
        'servicios': servicios,
        'destacados': destacados,
        'categorias': categorias,
        'indicators_range_carrusel1': indicators_range_carrusel1, # Nuevo
        'indicators_range_carrusel2': indicators_range_carrusel2, # Nuevo
        'indicators_range_carrusel3': indicators_range_carrusel3, # Nuevo
    })

def about(request):
    posts = CarrouselBanner.objects.filter(statusBanner=True)
    marcas = Marca.objects.filter(status=True)
    destacados = ProyectoDestacado.objects.select_related('proyecto').all()
    return render(request, 'publico/about/about.html', {
        'posts': posts,
        'marcas': marcas,
        'destacados': destacados,
    })

def project(request, project_id):
    proyecto = get_object_or_404(Proyecto, id=project_id)
    extra_projects = Proyecto.objects.exclude(id=project_id).order_by('?')[:3]
    return render(request, 'publico/about/proyecto.html', {
        'proyecto': proyecto,
        'extra_projects': extra_projects,
    })

def services(request):
    servicios = Servicio.objects.all()
    return render(request, 'publico/services/services.html', {
        'servicios': servicios,
    })

def store(request):
    destacados = ProductoDestacado.objects.select_related('producto').all()
    return render(request, 'publico/products/products.html', {
        'destacados': destacados,
    })


def products(request):
    marcas_qs = Marca.objects.filter(status=True)
    categorias_qs = Categoria.objects.filter(statusCategoria=True)

    qs = Producto.objects.all().order_by('id')

    search = request.GET.get('search', '').strip()
    if search:
        qs = qs.filter(producto_nombre__icontains=search)

    marcas = request.GET.getlist('marca')
    if marcas:
        qs = qs.filter(marca__id__in=marcas)

    categorias = request.GET.getlist('categoria')
    if categorias:
        qs = qs.filter(categoria__id__in=categorias)

    # --- Filtro de precio ---
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        qs = qs.filter(producto_precio_base__gte=precio_min)
    if precio_max:
        qs = qs.filter(producto_precio_base__lte=precio_max)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'productos': page_obj,
        'marcas': marcas_qs,
        'categorias': categorias_qs,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_products = render(request, 'publico/partials/_store_products.html', context).content.decode('utf-8')
        html_paginator = render(request, 'publico/partials/_store_paginator.html', context).content.decode('utf-8')
        return JsonResponse({
            'products_html': html_products,
            'paginator_html': html_paginator
        })

    return render(request, 'publico/store/store.html', context)

def products2(request, Nmarca):
    marcase = Marca.objects.filter(marca_name=Nmarca)
    idm=0
    for n in marcase:
        idm=n.id
        print(idm)
    marcas_qs = Marca.objects.filter(status=True)
    categorias_qs = Categoria.objects.filter(statusCategoria=True)

    qs = Producto.objects.filter(marca=idm).order_by('id')

    search = request.GET.get('search', '').strip()
    if search:
        qs = qs.filter(producto_nombre__icontains=search)

    marcas = request.GET.getlist('marca')
    if marcas:
        qs = qs.filter(marca__id__in=marcas)

    categorias = request.GET.getlist('categoria')
    if categorias:
        qs = qs.filter(categoria__id__in=categorias)

    # --- Filtro de precio ---
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        qs = qs.filter(producto_precio_base__gte=precio_min)
    if precio_max:
        qs = qs.filter(producto_precio_base__lte=precio_max)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'productos': page_obj,
        'marcas': marcas_qs,
        'categorias': categorias_qs,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_products = render(request, 'publico/partials/_store_products.html', context).content.decode('utf-8')
        html_paginator = render(request, 'publico/partials/_store_paginator.html', context).content.decode('utf-8')
        return JsonResponse({
            'products_html': html_products,
            'paginator_html': html_paginator
        })

    return render(request, 'publico/store/store.html', context)

def products3(request, Ncate):
    catese = Categoria.objects.filter(categoria_name=Ncate)
    idc=0
    for n in catese:
        idc=n.id
        print(idc)
    marcas_qs = Marca.objects.filter(status=True)
    categorias_qs = Categoria.objects.filter(statusCategoria=True)

    qs = Producto.objects.filter(categoria=idc).order_by('id')

    search = request.GET.get('search', '').strip()
    if search:
        qs = qs.filter(producto_nombre__icontains=search)

    marcas = request.GET.getlist('marca')
    if marcas:
        qs = qs.filter(marca__id__in=marcas)

    categorias = request.GET.getlist('categoria')
    if categorias:
        qs = qs.filter(categoria__id__in=categorias)

    # --- Filtro de precio ---
    precio_min = request.GET.get('precio_min')
    precio_max = request.GET.get('precio_max')
    if precio_min:
        qs = qs.filter(producto_precio_base__gte=precio_min)
    if precio_max:
        qs = qs.filter(producto_precio_base__lte=precio_max)

    paginator = Paginator(qs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'productos': page_obj,
        'marcas': marcas_qs,
        'categorias': categorias_qs,
    }

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html_products = render(request, 'publico/partials/_store_products.html', context).content.decode('utf-8')
        html_paginator = render(request, 'publico/partials/_store_paginator.html', context).content.decode('utf-8')
        return JsonResponse({
            'products_html': html_products,
            'paginator_html': html_paginator
        })

    return render(request, 'publico/store/store.html', context)

def product(request, sku):
    producto = get_object_or_404(Producto, producto_sku=sku)
    return render(request, 'publico/products/product.html', {'producto': producto})

def contacts(request):
    posts = CarrouselBanner.objects.filter(statusBanner=True)
    marcas = Marca.objects.filter(status=True)
    servicios = Servicio.objects.all()
    destacados = ProductoDestacado.objects.select_related('producto').all()  # <-- Agrega esta línea
    return render(request, 'publico/contacts/contacts.html', {
        'posts': posts,
        'marcas': marcas,
        'servicios': servicios,
        'destacados': destacados,  # <-- Y pásalo al template
    })

# Python
def search_products(request):
    query = request.GET.get('q', '').strip()
    productos = Producto.objects.filter(producto_nombre__icontains=query) if query else Producto.objects.none()
    results_html = render_to_string('publico/partials/_navbar_search_results.html', {'productos': productos})
    return JsonResponse({'results_html': results_html})


