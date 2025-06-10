# Barba_e_Navalha/models.py
from django.db import models

class Usuario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)
    senha = models.CharField(db_column='Senha', max_length=255, blank=True, null=True)
    tipo = models.TextField(db_column='Tipo', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Usuario'

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

class Local(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome_local = models.CharField(db_column='Nome_local', max_length=255, blank=True, null=True)
    endereco = models.CharField(db_column='Endereco', max_length=255, blank=True, null=True)
    cnpj = models.CharField(db_column='CNPJ', max_length=255, blank=True, null=True)
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)
    barbeirousuarioid = models.ForeignKey(Barbeiro, models.DO_NOTHING, db_column='BarbeiroUsuarioID', blank=True, null=True)
    # ### CAMPOS REMOVIDOS ###
    # idhorarios = models.ForeignKey('Horarios', models.DO_NOTHING, db_column='IDHorarios', blank=True, null=True)
    # idservicos = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='IDServicos', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Local'


class Servicos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)
    preco = models.DecimalField(db_column='Preco', max_digits=5, decimal_places=2, blank=True, null=True)
    duracao = models.IntegerField(db_column='Duracao', blank=True, null=True)
    # ### CAMPO ADICIONADO ###
    idlocal = models.ForeignKey('Local', models.DO_NOTHING, db_column='IDLocal', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Servicos'


class Horarios(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    dia_semana = models.CharField(db_column='Dia_semana', max_length=7, blank=True, null=True)
    hora_inicio = models.TimeField(db_column='Hora_inicio', blank=True, null=True)
    hora_fim = models.TimeField(db_column='Hora_fim', blank=True, null=True)
    # ### CAMPO ADICIONADO ###
    idlocal = models.ForeignKey('Local', models.DO_NOTHING, db_column='IDLocal', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Horarios'

class Agenda(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)
    data = models.DateField(db_column='Data', blank=True, null=True)
    hora = models.TimeField(db_column='Hora', blank=True, null=True)
    idbarbeiro = models.ForeignKey('Barbeiro', models.DO_NOTHING, db_column='IDBarbeiro', blank=True, null=True)
    idcliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='IDCliente', blank=True, null=True)
    idservicos = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='IDServicos', blank=True, null=True)
    google_calendar_event_id = models.CharField(db_column='GoogleCalendarEventID', max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'Agenda'

class GoogleApiToken(models.Model):
    # Relacionamento com seu modelo de usuário ou barbeiro
    # Usando OneToOneField para garantir que cada barbeiro tenha apenas um conjunto de tokens
    barbeiro = models.OneToOneField(Barbeiro, on_delete=models.CASCADE, primary_key=True)
    # Campos para armazenar as credenciais obtidas do Google
    token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255, null=True, blank=True)
    token_uri = models.CharField(max_length=255)
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scopes = models.TextField()

    class Meta:
        managed = True # Deixe o Django gerenciar esta tabela
        db_table = 'GoogleApiToken'