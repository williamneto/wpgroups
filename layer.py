# -*- coding: utf-8 -*-

# CRIANDO GRUPOS DE WHATSAPP
# Usando a biblioteca Yowsup para criar grupos de de whatsapp

from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.common.tools import Jid

# Array com os numeros que serao adicionados ao grupo,
# com o codigo do pais (55 para BR) e DDD
# ex ["5521xxxxxxxxx","5521xxxxxxxxx"]
numeros = []

# Array com numeros dos membros dos grupos que serao
# administradores do grupo
admins = []

class CreateGroupsLayer(YowInterfaceLayer):
	@ProtocolEntityCallback("success")
	def onSuccess(self, successProtocolEntity):
		# Usa uma ferramenta da biblioteca que converte
		# os numeros de telefones para o padrao usado internamente
		# no whatsapp adicionando um sufixo
		jids = [Jid.normalize(number) for number in numeros]

		# Titulo que o grupo tera
		titulo = "#DevsOnBeer"

		# Cria o grupo
		grupo = CreateGroupsIqProtocolEntity(titulo, participants=jids)
		self.toLower(grupo)
		print(">> Grupo %s criado\n" % titulo)

		def onGroupsListResult(successEntity, originalEntity):
			# Seleciona e percorre todos os grupos que faz parte
			meusGrupos = [ grupo for grupo in successEntity.getGroups()]
			for grupo in meusGrupos:
				# Seleciona apenas o grupo com o titulo recem criado
				# e promove os numeros do array admin a moderadores
				if grupo.getSubject() == titulo:
					entity = PromoteParticipantsIqProtocolEntity(Jid.normalize(grupo.getId()), [Jid.normalize(number) for number in admins])
					self.toLower(entity)	
					print(">> Membros promovidos a moderadores\n")		
		def onGroupsListError(errorEntity, originalEntity):
			print error		

		entity = ListGroupsIqProtocolEntity()
		successFn = lambda successEntity, originalEntity: onGroupsListResult(successEntity, originalEntity)
		errorFn = lambda errorEntity, originalEntity: ononGroupsListError(errorEntity, originalEntity)
		self._sendIq(entity, successFn, errorFn)

	@ProtocolEntityCallback("receipt")
	def onReceipt(self, entity):
		self.toLower(entity.ack())	

		
