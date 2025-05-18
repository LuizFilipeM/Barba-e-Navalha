from django.db import models

# Definição dos tipos ENUM para Django
class TipoUsuario(models.TextChoices):
    CLIENTE = 'Cliente', 'Cliente'
    BARBEIRO = 'Barbeiro', 'Barbeiro'
    ADMIN = 'Admin', 'Admin'

class Usuario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)   
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)         
    senha = models.CharField(db_column='Senha', max_length=255, blank=True, null=True)         
    tipo = models.TextField(db_column='Tipo', blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'Usuario'

class Cliente(models.Model):
    id = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='ID', primary_key=True)   
    cpf = models.CharField(db_column='CPF', max_length=14, blank=True, null=True)   
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)           
    cidade = models.CharField(db_column='Cidade', max_length=255, blank=True, null=True)       
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)    
    data_nascimento = models.DateField(db_column='Data_Nascimento', blank=True, null=True)     

    class Meta:
        managed = False
        db_table = 'Cliente'

class Barbeiro(models.Model):
    id = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='ID', primary_key=True)   
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)           
    cpf = models.CharField(db_column='CPF', max_length=14, blank=True, null=True)   
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)    
    data_nascimento = models.DateField(db_column='Data_Nascimento', blank=True, null=True)     
    cidade = models.CharField(db_column='Cidade', max_length=255, blank=True, null=True)       

    class Meta:
        managed = False
        db_table = 'Barbeiro'

class Servicos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)   
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)           
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)   
    preco = models.DecimalField(db_column='Preco', max_digits=5, decimal_places=2, blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'Servicos'

class Agenda(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)   
    data = models.DateField(db_column='Data', blank=True, null=True)   
    hora = models.TimeField(db_column='Hora', blank=True, null=True)   
    idbarbeiro = models.ForeignKey('Barbeiro', models.DO_NOTHING, db_column='IDBarbeiro', blank=True, null=True)   
    idcliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='IDCliente', blank=True, null=True)   
    idservico = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='IDServico', blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'Agenda'

class Horarios(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)   
    dia_semana = models.CharField(db_column='Dia_semana', max_length=7, blank=True, null=True)   
    horarios = models.TimeField(db_column='Horarios', blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'Horarios'

class Local(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)   
    nome_local = models.CharField(db_column='Nome_local', max_length=255, blank=True, null=True)   
    endereco = models.CharField(db_column='Endereco', max_length=255, blank=True, null=True)   
    cnpj = models.CharField(db_column='CNPJ', max_length=255, blank=True, null=True)           
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)    
    idhorarios = models.ForeignKey(Horarios, models.DO_NOTHING, db_column='IDHorarios', blank=True, null=True)   
    idservicos = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='IDServicos', blank=True, null=True)   
    barbeirousuarioid = models.ForeignKey(Barbeiro, models.DO_NOTHING, db_column='BarbeiroUsuarioID', blank=True, null=True)   

    class Meta:
        managed = False
        db_table = 'Local'