# APP para consultar disponibilidade no SUS

App para consultar disponibilidade no SUS pelo nome genérico do medicamento.

## Requisitos

- Ao entrar no app o usuário vê apenas uma tela com um campo de busca e um botão escrito buscar.
- Ao digitar no campo de busca pelo nome genêrico do medicamento, o app faz as seguintes validações:
    - O usuário realmente digitou algo?
- Após validar o que o usuário digitou, o app checa se o medicamento está no banco de dados.
- Se o medicamento está no banco de dados, o app mostra na tela uma tabela com todos os medicamentos encontrados. Na tabela contém nome genérico, concentração/composição, forma farmacêutica, codigo atc e componente.
- Se o medicamento não está no banco de dados, o app mostra na tela uma mensagem dizendo que o medicamento não foi encontrado.

## Setup inicial

- Projeto testado em Windows 11 com Python 3.11.0.

- No console:
```bash
<python_path> -m venv env
. env/Scripts/activate
python.exe -m pip install --upgrade pip
pip install django
pip install djangorestframework
pip install markdown  
pip install django-filter
pip install pillow
pip install django-cors-headers
django-admin startproject core .
python manage.py startapp medicines
python manage.py migrate
python manage.py createsuperuser
```
- Em *core/settings.py* acrescente `'medicines'` em `INSTALED_APPS`.
- Em *core/settings.py* acrescente `'rest_framework'` em `INSTALED_APPS`.
- Em *core/settings.py* acrescente `'corsheaders'` em `INSTALED_APPS`.
- Em *core/settings.py* adicione os seguintes Middlewares:
```python
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
```
- Em *core/settings.py* acrescente `CORS_ALLOW_ALL_ORIGINS = True`.
- Crie o arquivo *requirements.txt*: `pip freeze > requirements.txt`

## Model

- ChatGPT: Faça um modelo Medicine com campos denominacao_generica, concentracao_composicao, forma_farmaceutica, codigo_atc e componente para Django.
```python
from django.db import models

class Medicine(models.Model):
    denominacao_generica = models.CharField(max_length=222)
    concentracao_composicao = models.CharField(max_length=222)
    forma_farmaceutica = models.CharField(max_length=222)
    codigo_atc = models.CharField(max_length=222)
    componente = models.CharField(max_length=222)
    
    def __str__(self):
        return self.denominacao_generica
```
- No console:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Admin

- ChatGPT: Faça um script no *admin.py* para que seja possível, no painel do admin, visualizar id, denominação genérica e concentração/composição.
```python
from django.contrib import admin
from .models import Medicine

class MedicineAdmin(admin.ModelAdmin):
    list_display = ('id', 'denominacao_generica', 'concentracao_composicao')
    
admin.site.register(Medicine, MedicineAdmin)
```

- Rode o servidor: `python manage.py runserver`
- Acesse a url do admin: `http://localhost:8000/admin`
- Faça login e insira pelo menos 3 medicamentos.
- Abra o banco de dados com Dbeaver e veja se os registros foram devidamente inseridos.

## Serializers

- Em *medicines/serializers.py* crie a serialização para o model *Medicine*:
```python
from rest_framework.serializers import ModelSerializer
from .models import Medicine


class MedicineSerializer(ModelSerializer):
  class Meta:
    model = Medicine
    fields = '__all__'
```

## Url + View da api de lista de medicamentos

- Em *core/urls.py* adicione a seguinte url: `path('api/medicines/', ListMedicines.as_view())`
- Em *core/urls.py* import de *medicines/api/views.py* a view `ListMedicines`.
- Crie o arquivo *medicines/api/\_\_init\_\_.py*

- Em *medicines/api/views.py* crie a view `ListMedicines`:
```python
from ..serializers import MedicineSerializer
from ..models import Medicine
from rest_framework import generics


class ListMedicines(generics.ListAPIView):

  queryset = Medicine.objects.all()
  serializer_class = MedicineSerializer
```

- A api está pronta para listar as tarefas. Teste usando algum aplicativo, por exemplo o Insomnia (para Windows) ou o Postman (Windows, Mac e Linux).

- **TAREFA:** Faça uma adaptação no código para que a api aceite também uma requisão POST para inserir novos medicamentos no banco dados.

## URL + VIEW (Parte 1): Renderize a página principal

- Em *core/urls.py* adicione a seguinte url: `path('', list_medicines, name='list_medicines')`
- Em *core/urls.py* import de *medicines/html/views.py* a function view `list_medicines`.
- Em *medicines/html/views.py* crie a function view `list_medicines`:
```python
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..models import Medicine

@require_http_methods(["GET"])
def list_medicines(request):
    return render(request, 'index.html')
```

- Crie o arquivo *medicines/templates/index.html*.
```html
    <form>
        <input type="text" name="denominacao_generica" required>
        <button>Buscar</button>
    </form>
```

## URL + VIEW (Parte 2): Retorne a tabela na submissão do formulário

- - Em *medicines/html/views.py* altere a function view `list_medicines`:
```python
from django.shortcuts import render
from django.views.decorators.http import require_http_methods

from ..models import Medicine

@require_http_methods(["GET", "POST"])
def list_medicines(request):
    if request.method == "POST":
        denomicao_generica = request.POST.get(
            'denomicao_generica'
        )
        medicines = Medicine.objects.filter(
            denomicao_generica=denomicao_generica
        )
        context = {"medicines": medicines}
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
```

- Crie o arquivo *medicines/templates/index.html*.
```html
    <form action="{% url 'list_medicines' %}" method="POST">
        {% csrf_token %}
        <input type="text" name="denominacao_generica" required>
        <button>Buscar</button>
    </form>

    {% if medicines %}
        <table>
            <tr>
                <th>Descrição genérica</th>
                <th>Concentração/composição</th>
                <th>Fórmula farmacêutica</th>
                <th>Código ATC</th>
                <th>Componente</th>
            </tr>
        {% for medicine in medicines %}
            <tr>
                <td>{{medicine.denominacao_generica}}</td>
                <td>{{medicine.concentracao_composicao}}</td>
                <td>{{medicine.forma_farmaceutica}}</td>
                <td>{{medicine.codigo_atc}}</td>
                <td>{{medicine.componente}}</td>
            </tr>
        {% endfor %}
        </table>
    {% else %}
        {% if search_message %}
            <p>{{search_message}}</p>
        {% endif %}
    {% endif %}
```

## Estáticos

- Crie o arquivo *static/css/style.css*
- Em *core/settings.py*:
```python
import os

STATIC_URL = '/static/'
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'), )
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```
- Em *core/urls.py*:
```python
from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
```

-Faça a conexão do *style.css* com o *index.html*:
```html
{% load static %}
<html>
    <head>
        <link rel="stylesheet" type="text/css" href="{% static 'css/style.css' %}" />
    </head>
    <body>
        ...
    </body>
</html>
```

- Faça os estilos ao seu gosto! Exemplo:

```css
body {
    background: #fefefe;
    max-width: 800px;
    margin: 64px auto;
}

table {
    margin-top: 16px;
}

td, th {
    border: 1px solid #ddd;
    padding: 8px;
}
  
tr:nth-child(even){background-color: #f2f2f2;}
  
tr:hover {background-color: #ddd;}
  
th {
    padding-top: 12px;
    padding-bottom: 12px;
    text-align: left;
    background-color: #06D6A0;
    color: white;
}

button {
    background: #06D6A0;
    color: #fff;
    outline: none;
    border: none;
    padding: 2px 8px;
}

p {
    font-size: 1.2rem;
    color: #EF476F;
    font-weight: bold;
}
```
