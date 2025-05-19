from django.db import models

class Usuario(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=255, blank=True, null=True)  # Field name made lowercase.
    senha = models.CharField(db_column='Senha', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tipo = models.TextField(db_column='Tipo', blank=True, null=True)  # Field name made lowercase. This field type is a guess.

    class Meta:
        managed = False
        db_table = ''

class Barbeiro(models.Model):
    id = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=14, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)  # Field name made lowercase.
    data_nascimento = models.DateField(db_column='Data_Nascimento', blank=True, null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Barbeiro'

class Cliente(models.Model):
    id = models.OneToOneField('Usuario', models.DO_NOTHING, db_column='ID', primary_key=True)  # Field name made lowercase.
    cpf = models.CharField(db_column='CPF', max_length=14, blank=True, null=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cidade = models.CharField(db_column='Cidade', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)  # Field name made lowercase.
    data_nascimento = models.DateField(db_column='Data_Nascimento', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Cliente'

class Servicos(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome = models.CharField(db_column='Nome', max_length=255, blank=True, null=True)  # Field name made lowercase.
    descricao = models.CharField(db_column='Descricao', max_length=255, blank=True, null=True)  # Field name made lowercase.
    preco = models.DecimalField(db_column='Preco', max_digits=5, decimal_places=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Servicos'

class Local(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    nome_local = models.CharField(db_column='Nome_local', max_length=255, blank=True, null=True)  # Field name made lowercase.
    endereco = models.CharField(db_column='Endereco', max_length=255, blank=True, null=True)  # Field name made lowercase.
    cnpj = models.CharField(db_column='CNPJ', max_length=255, blank=True, null=True)  # Field name made lowercase.
    telefone = models.CharField(db_column='Telefone', max_length=16, blank=True, null=True)  # Field name made lowercase.
    idhorarios = models.ForeignKey('Horarios', models.DO_NOTHING, db_column='IDHorarios', blank=True, null=True)  # Field name made lowercase.
    idservicos = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='IDServicos', blank=True, null=True)  # Field name made lowercase.
    barbeirousuarioid = models.ForeignKey(Barbeiro, models.DO_NOTHING, db_column='BarbeiroUsuarioID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Local'

class Horarios(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    dia_semana = models.CharField(db_column='Dia_semana', max_length=7, blank=True, null=True)  # Field name made lowercase.
    hora_inicio = models.TimeField(db_column='Hora_inicio', blank=True, null=True)  # Field name made lowercase.
    hora_fim = models.TimeField(db_column='Hora_fim', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Horarios'

class Agenda(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.
    data = models.DateField(db_column='Data', blank=True, null=True)  # Field name made lowercase.
    hora = models.TimeField(db_column='Hora', blank=True, null=True)  # Field name made lowercase.
    idbarbeiro = models.ForeignKey('Barbeiro', models.DO_NOTHING, db_column='IDBarbeiro', blank=True, null=True)  # Field name made lowercase.
    idcliente = models.ForeignKey('Cliente', models.DO_NOTHING, db_column='IDCliente', blank=True, null=True)  # Field name made lowercase.
    idservicos = models.ForeignKey('Servicos', models.DO_NOTHING, db_column='IDServicos', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Agenda'