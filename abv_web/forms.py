from django import forms
from django.forms import ModelForm

from abv_web.models import *


#---------------------------------------------CRUD MARCAS----------------------------------------------------------#
class MarcaForm(forms.ModelForm):
    class Meta:
        model = Marca
        fields = ['marca_name', 'marca_url_img', 'marca_descripcion']

    marca_name = forms.CharField(
        label="Nombre de la Marca",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    marca_url_img = forms.ImageField(
        label="Imagen",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )
    marca_descripcion = forms.CharField(
        label="Descripción de la marca",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        max_length=300
    )

#------------------------------------------CRUD CATEGORIAS---------------------------------------------------------#

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Categoria
        fields = ['categoria_name', 'categoria_url_img', 'categoria_descripcion']

    categoria_name = forms.CharField(
        label="Nombre de la Marca",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    categoria_url_img = forms.ImageField(
        label="Imagen",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )
    categoria_descripcion = forms.CharField(
        label="descripción de la categoria",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        max_length=300
    )

#------------------------------------------CRUD CARROUSELBANNER-----------------------------------------------------#

class CarrouselBannerForm(forms.ModelForm):
    class Meta:
        model = CarrouselBanner
        fields = ['carrouselBanner_name', 'carrouselBanner_url_img', 'carrouselBanner_descripcion']

    carrouselBanner_name = forms.CharField(
        label="Nombre de la Marca",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    carrouselBanner_url_img = forms.ImageField(
        label="Imagen",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )
    carrouselBanner_descripcion = forms.CharField(
        label="descripción de la categoria",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        max_length=300
    )


#------------------------------------------CRUD USUARIOS-----------------------------------------------------------#

class UsuarioForm(forms.ModelForm):
    username = forms.CharField(
        label='Nombre de usuario',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label='Correo electrónico',
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    first_name = forms.CharField(
        label='Nombre',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        label='Apellido',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        required=False,
        help_text='La contraseña debe tener al menos 8 caracteres.'
    )
    is_active = forms.BooleanField(
        label='Activo',
        required=False,
        widget=forms.CheckboxInput()
    )
    is_superuser = forms.BooleanField(
        label='Super Usuario',
        required=False,
        widget=forms.CheckboxInput()
    )

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'is_active', 'is_superuser']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_password(self):
        password = self.cleaned_data.get('password', '')
        if password and len(password) <= 8:
            raise forms.ValidationError(
                'Para mantener la seguridad, la contraseña debe tener al menos 8 caracteres. Ingrese una contraseña válida o repita la existente para mantenerla sin cambios.'
            )
        return password
#------------------------------------------CRUD TIENDA------------------------------------------------------------#

class TiendaForm(forms.ModelForm):
    tienda_enlace = forms.URLField(
        label='Enlace de la tienda',
        widget=forms.URLInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: https://FuseTech.com'
        }),
        help_text='Asegúrate de incluir http:// o https:// al inicio del enlace.'
    )
    tienda_nombre = forms.CharField(
        label='Nombre de la tienda',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ejemplo: FuseTech Componentes'
        }),
        max_length=30
    )
    tienda_descripcion = forms.CharField(
        label='Descripción de la tienda',
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 3,
            'placeholder': 'Ejemplo: Expertos en fusibles, transformadores y circuitos para todo tipo de proyectos eléctricos.'
        }),
        max_length=300
    )
    tienda_imagen = forms.ImageField(
        label='Imagen de la tienda',
        required=False,
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'placeholder': 'Selecciona una imagen representativa de la tienda'
        }),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )

    class Meta:
        model = Tienda
        fields = [
            'tienda_enlace',
            'tienda_nombre',
            'tienda_descripcion',
            'tienda_imagen'
        ]

    def clean_tienda_enlace(self):
        enlace = self.cleaned_data.get('tienda_enlace', '')
        # Si el usuario no escribe http:// o https://, lo anteponemos
        if enlace and not enlace.startswith(('http://', 'https://')):
            enlace = 'http://' + enlace
        return enlace


#------------------------------------------CRUD EMPRESA-----------------------------------------------------------#

class EmpresaForm(forms.ModelForm):
    empresa_nombre = forms.CharField(
        label="Nombre de la Empresa",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    empresa_descripcion = forms.CharField(
        label="Descripción de la Empresa",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        max_length=300
    )
    empresa_logo = forms.ImageField(
        label="Logo",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )

    class Meta:
        model = Empresa
        fields = ['empresa_nombre', 'empresa_descripcion', 'empresa_logo']

#------------------------------------------CRUD ALMACEN-----------------------------------------------------------#

class AlmacenForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        label="Empresa encargada del Almacén",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    almacen_nombre = forms.CharField(
        label="Nombre del Almacén",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    almacen_direccion_calle = forms.CharField(
        label="Calle",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=300
    )
    almacen_direccion_numero = forms.CharField(
        label="Número",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    almacen_direccion_colonia = forms.CharField(
        label="Colonia",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    almacen_direccion_cp = forms.CharField(
        label="Código Postal",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    almacen_direccion_ciudad = forms.CharField(
        label="Ciudad",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )
    almacen_direccion_estado = forms.CharField(
        label="Estado",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=30
    )

    class Meta:
        model = Almacen
        fields = [
            'empresa',
            'almacen_nombre',
            'almacen_direccion_calle',
            'almacen_direccion_numero',
            'almacen_direccion_colonia',
            'almacen_direccion_cp',
            'almacen_direccion_ciudad',
            'almacen_direccion_estado',
        ]

#------------------------------------------CRUD ALMACEN-----------------------------------------------------------#

class ProductoForm(forms.ModelForm):
    producto_extendido = forms.CharField(
        label='Producto Extendido',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30
    )
    producto_sku = forms.CharField(
        label='SKU',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30
    )
    producto_skunetsuite = forms.CharField(
        label='SKU Netsuite',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=300
    )
    producto_ean = forms.CharField(
        label='EAN',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30
    )
    producto_nombre = forms.CharField(
        label='Nombre del Producto',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30
    )
    producto_descripcion = forms.CharField(
        label='Descripción',
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        max_length=300
    )
    producto_modelo = forms.CharField(
        label='Modelo',
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=30
    )
    producto_precio_base = forms.DecimalField(
        label='Precio Base',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_digits=10,
        decimal_places=2
    )
    producto_precio_amazon = forms.DecimalField(
        label='Precio Amazon',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_digits=10,
        decimal_places=2
    )
    producto_precio_mercadolibre = forms.DecimalField(
        label='Precio MercadoLibre',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_digits=10,
        decimal_places=2
    )
    producto_precio_ebay = forms.DecimalField(
        label='Precio eBay',
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        max_digits=10,
        decimal_places=2
    )
    producto_url_img = forms.ImageField(
        label='Imagen del Producto',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )
    marca = forms.ModelChoiceField(
        queryset=Marca.objects.all(),
        label='Marca',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    categoria = forms.ModelChoiceField(
        queryset=Categoria.objects.all(),
        label='Categoría',
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Producto
        fields = [
            'producto_extendido', 'producto_sku', 'producto_skunetsuite', 'producto_ean', 'producto_nombre',
            'producto_descripcion', 'producto_modelo', 'producto_precio_base', 'producto_precio_amazon',
            'producto_precio_mercadolibre', 'producto_precio_ebay',
            'producto_url_img', 'marca', 'categoria'
        ]

#------------------------------------------CRUD SERVICIOS----------------------------------------------------------#

class ServicioForm(forms.ModelForm):
    servicio_nombre = forms.CharField(
        label="Titulo del Servicio",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=50
    )
    servicio_descripcion = forms.CharField(
        label="Descripción del Servicio",
        required=False,
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        max_length=300
    )
    servicio_imagen = forms.ImageField(
        label="Imagen descriptiva",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )

    class Meta:
        model = Servicio
        fields = ['servicio_nombre', 'servicio_descripcion', 'servicio_imagen']

#------------------------------------------CRUD PROYECTOS----------------------------------------------------------#

class ProyectoForm(forms.ModelForm):
    proyecto_nombre = forms.CharField(
        label="Título del Proyecto",
        widget=forms.TextInput(attrs={"class": "form-control"}),
        max_length=50
    )
    proyecto_descripcion_corta = forms.CharField(
        label="Descripción Corta",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        max_length=300
    )
    proyecto_descripcion_larga = forms.CharField(
        label="Descripción Larga",
        widget=forms.Textarea(attrs={"class": "form-control", "rows": 6}),
        max_length=1000
    )
    proyecto_imagen = forms.ImageField(
        label="Imagen del Proyecto",
        required=False,
        widget=forms.FileInput(attrs={"class": "form-control"}),
        help_text='Formato permitido: JPG, PNG. Tamaño máximo: 5MB.'
    )

    class Meta:
        model = Proyecto
        fields = [
            "proyecto_nombre",
            "proyecto_descripcion_corta",
            "proyecto_descripcion_larga",
            "proyecto_imagen"
        ]

#------------------------------------------CRUD DESTACADOS----------------------------------------------------------#

class DestacadoForm(forms.Form):
    productos = forms.ModelMultipleChoiceField(
        queryset=Producto.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-control'}),
        label='Selecciona productos destacados'
    )

#------------------------------------------CRUD DESTACADOS----------------------------------------------------------#

class InventarioForm(forms.ModelForm):
    almacen = forms.ModelChoiceField(
        queryset=Almacen.objects.all(),
        label="Almacén",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    stock = forms.IntegerField(
        label="Stock",
        min_value=0,
        widget=forms.NumberInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Inventario
        fields = ['almacen', 'stock']