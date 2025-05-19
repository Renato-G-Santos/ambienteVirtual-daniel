from django.shortcuts import render, redirect, get_object_or_404
from app.models import Usuario, Produto
from app.forms import formUsuario, formProduto, formLogin
from datetime import timedelta
#import requests

# Página inicial
def home(request):
    return render(request, "template.html")

# Página de login

# ========== USUÁRIOS ==========

# Exibir todos os usuários
def exibirUsuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, "usuario.html", {'listUsuarios': usuarios})

# Adicionar novo usuário
def addUsuario(request):
    if request.method == "POST":
        formUser = formUsuario(request.POST)
        if formUser.is_valid():
            formUser.save()
            print("Usuário cadastrado com sucesso!")
            return redirect('exibirUsuarios')
        else:
            print("Formulário inválido:", formUser.errors)
    else:
        formUser = formUsuario()

    return render(request, "add-usuario.html", {'form': formUser})

# Editar usuário
def editarUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    formUser = formUsuario(request.POST or None, instance=usuario)

    if request.method == "POST":
        if formUser.is_valid():
            formUser.save()
            return redirect("exibirUsuarios")

    return render(request, "editar-usuario.html", {'form': formUser})

# Excluir usuário
def excluirUsuario(request, id_usuario):
    usuario = Usuario.objects.get(id=id_usuario)
    usuario.delete()
    return redirect("exibirUsuarios")

# ========== PRODUTOS ==========

# Listar produtos
def listar_produtos(request):
    if request.session.get("email") is None:
        return redirect('login')
    produtos = Produto.objects.all()
    return render(request, "produtos/listar_produtos.html", {'produtos': produtos})

#bloquear o acesso a essa página se o usuário não estiver logado

# Cadastrar produto
def cadastrar_produto(request):
    if request.session.get("email") is None:
        return redirect('login')
    
    if request.method == 'POST':
        form = formProduto(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = formProduto()
    return render(request, 'produtos/cadastrar_produto.html', {'form': form})

# Editar produto
def editar_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    if request.method == 'POST':
        form = formProduto(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('listar_produtos')
    else:
        form = formProduto(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form})

def buscar_cep(request):
    if request.method == 'POST':
        cep = request.POST.get('cep')
        url = f'https://viacep.com.br/ws/{cep}/json/'
        response = requests.get(url)
        data = response.json()

        if 'erro' not in data:
            form = formUsuario(initial={
                'logradouro': data.get('logradouro'),
                'bairro': data.get('bairro'),
                'cidade': data.get('localidade'),
                'estado': data.get('uf')
            })
            return render(request, 'add-usuario.html', {'form': form})
        else:
            print("CEP inválido ou não encontrado.")
    
    return 1


# Excluir produto
def excluir_produto(request, id):
    produto = get_object_or_404(Produto, pk=id)
    produto.delete()

def login(request): 
    if buscar_cep(request) != 1:
        return redirect('addUsuario')
    frmLogin = formLogin(request.POST or None)
    if request.POST: 
        if frmLogin.is_valid():
            _email = frmLogin.cleaned_data.get('email')
            _senha = frmLogin.cleaned_data.get('senha')
            try:
                userLogin = Usuario.objects.get(email=_email, senha=_senha)
                if userLogin is not None:
                    request.session.set_expiry(timedelta(seconds=60))
                    request.session["email"] = userLogin.email

                    return redirect('dashboard')
            except Usuario.DoesNotExist:
                return render(request, "login.html", {'form': frmLogin, 'error': 'Usuário ou senha inválidos.'})
    return render(request, "login.html", {'form': frmLogin})

def dashboard(request):
    _email = request.session.get("email")
    return render(request, "dashboard.html", {'email': _email})

def quem_somos(request):
    return render(request, "quem_somos.html")

def produtos_card(request):
    produtosapi = request.get("https://fakestoreapi.com/products").json()
    return render(request, "produtos/produtos_card.html", {'produtos': produtosapi})


def logout(request):
    request.session.flush()
    return redirect('home')
