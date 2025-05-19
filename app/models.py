from django.db import models

# Model para usuários
class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()
    senha = models.CharField(max_length=16)
    endereco = models.CharField(max_length=255)
    bairro = models.CharField(max_length=100)
    cidade = models.CharField(max_length=100)
    estado = models.CharField(max_length=100)
    cep = models.CharField(max_length=10)
    numero_residencia = models.CharField(max_length=10)
    localidade = models.CharField(max_length=100)


# Model para produtos
class Produto(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    foto = models.ImageField(upload_to='produtos/')
    estoque = models.PositiveIntegerField()

    def __str__(self):
        return self.nome

# class usuario(models.Model):
#     nome = models.CharField(max_length=100)
#     email = models.EmailField()
#     senha = models.CharField(max_length=16)

#     def __str__(self):
#         return f"{self.nome} ({self.email})"

