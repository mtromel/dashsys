from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from datetime import date

class Maquina(models.Model):
    TIPO_CHOICES = [
        ('DOBRADEIRA', 'Dobradeira'),
        ('LASER', 'Laser'),
    ]

    matricula_br = models.CharField("Matrícula GDB", max_length=25, unique=True)
    modelo_maq = models.CharField("Modelo da Máquina", max_length=60, null=True, blank=True)
    cliente = models.CharField("Cliente", max_length=100)
    data_entrega_ch = models.DateField("Data de Entrega Estimada CH", default=None)
    data_embarque = models.DateField("Data de Embarque CH", default=None)
    data_chegada_br = models.DateField("Data de Chegada BR", default=None)
    data_entrega_cliente = models.DateField("Data de Entrega Cliente", default=None)
    tipo = models.CharField("Tipo de Máquina", max_length=15, choices=TIPO_CHOICES)
    exibir_no_dashboard = models.BooleanField(default=True, verbose_name="Exibir na TV?")

    def __str__(self):
        return f"{self.matricula_br} - {self.cliente}"
    
    # Lógica para destacar atraso
    @property
    def esta_atrasada(self):
        if self.data_entrega_cliente and self.data_entrega_cliente < date.today():
            return True
        return False

class Apontamento(models.Model):
    maquina = models.ForeignKey(Maquina, on_delete=models.CASCADE, related_name='apontamento')

    # CAMPOS COMUNS (Presentes em ambos os tipos)
    data_entrega_ch = models.BooleanField("Entrega China realizada", default=False)
    data_embarque = models.BooleanField("Embarque realizado", default=False)
    data_chegada_br = models.BooleanField("Entregue na fábrica", default=False)
    testes = models.BooleanField("Testes concluídos", default=False)
    carregamento = models.BooleanField("Carregamento realizado", default=False)
    # vistoria_final = models.BooleanField("Vistoria Final", default=False)
    # ade_nr12 = models.BooleanField("Adequação NR-12", default=False)

    # CAMPOS ESPECÍFICOS: DOBRADEIRA
    # Grupo: Montagem
    # dob_start_eletrico = models.BooleanField("Start Elétrico", default=False)
    # # Grupo: Configuração e Testes
    # dob_regulagem = models.BooleanField("Regulagem", default=False)
    # dob_teste_dobra = models.BooleanField("Teste de Dobra", default=False)

    # CAMPOS ESPECÍFICOS: LASER
    # # Grupo: Montagem Geral
    # las_nivelamento = models.BooleanField("Nivelamento", default=False)
    # las_montagem_cabecote = models.BooleanField("Montagem Estrutura Cabeçote", default=False)
    # las_posicionamento_perif = models.BooleanField("Posicionamento Periféricos", default=False)
    # # Grupo: Elétrica
    # las_passagem_fibra = models.BooleanField("Passagem Fibra Óptica", default=False)
    # las_montagem_cab_elet = models.BooleanField("Montagem Cabeçote (Elétrica)", default=False)
    # las_alimentacao = models.BooleanField("Alimentação da Máquina", default=False)
    # # Grupo: Configuração e Testes
    # las_alin_cabecote = models.BooleanField("Alinhamento Cabeçote", default=False)
    # las_alin_bico = models.BooleanField("Alinhamento Bico", default=False)
    # las_testes_corte = models.BooleanField("Testes de Corte", default=False)

    # --- LÓGICA DE CÁLCULO (PESOS) ---

    def _calc_percent(self, campos):
        """Função auxiliar: recebe lista de booleanos e retorna % de conclusão."""
        if not campos: return 0
        concluidos = sum(1 for c in campos if c)
        return (concluidos / len(campos)) * 100

    @property
    def progresso_por_grupo(self):
        """Retorna um dicionário com os percentuais de cada grupo conforme o tipo."""
        res = {}
        res['Entrega CH'] = self._calc_percent([self.data_entrega_ch])
        res['Embarque'] = self._calc_percent([self.data_embarque])
        res['Entrega BR'] = self._calc_percent([self.data_chegada_br])
        res['Testes'] = self._calc_percent([self.testes])
        res['Carregamento'] = self._calc_percent([self.carregamento])
        # if self.maquina.tipo == 'DOBRADEIRA':
        #     res['Montagem'] = self._calc_percent([self.dob_start_eletrico])
        #     res['Configuração e Testes'] = self._calc_percent([self.dob_regulagem, self.dob_teste_dobra])
        #     res['Adequação e Vistoria'] = self._calc_percent([self.ade_nr12, self.vistoria_final])
        # else: # LASER
        #     res['Montagem Geral'] = self._calc_percent([self.las_nivelamento, self.las_montagem_cabecote, self.las_posicionamento_perif])
        #     res['Elétrica'] = self._calc_percent([self.las_passagem_fibra, self.las_montagem_cab_elet, self.las_alimentacao])
        #     res['Configuração e Testes'] = self._calc_percent([self.las_alin_cabecote, self.las_alin_bico, self.las_testes_corte])
        #     res['Adequação e Vistoria'] = self._calc_percent([self.ade_nr12, self.vistoria_final])
        return res

    @property
    def total_geral(self):
        """Calcula a média simples dos percentuais dos grupos (pesos iguais)."""
        grupos = self.progresso_por_grupo.values()
        return sum(grupos) / len(grupos) if grupos else 0
    
    def __str__(self):
        return f" {self.maquina.matricula_br}"

@receiver(post_save, sender=Maquina)
def criar_apontamento(sender, instance, created, **kwargs):
    if created:
        Apontamento.objects.create(maquina=instance)