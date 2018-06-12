# -*- coding: utf-8 -*-

# CRIANDO GRUPOS DE WHATSAPP
# Usando a biblioteca Yowsup para criar grupos de de whatsapp

from yowsup.layers.protocol_groups.protocolentities      import *
from yowsup.layers.interface import YowInterfaceLayer, ProtocolEntityCallback
from yowsup.common.tools import Jid
from yowsup.layers.protocol_presence.protocolentities    import *


import sys
reload(sys)
sys.setdefaultencoding('utf8')

class CadastroLayer(YowInterfaceLayer):
	def __init__(self):
		super(CadastroLayer, self).__init__()
		self.resp = [
			"Ola, seja bem vindo! Preciso de algumas informaçoes suas. Primeiro, qual o seu nome?",
			"Ok %s, em que cidade voce mora?",
			"otimo, e em qual bairro?",
			"Tudo certo! Agora so salvar meu numero nos seus contatos que vc vai receber informaçoes! ",
			"Vc ja esta cadastrado, quando tiver novidades te passo"
		]

		# dois controladores para permitir conversas simultaneas
		# registra com quais numeros esta conversando
		self.conv_with = []
		# registra o estagio da conversa com cada um deles
		self.conv_stage = {}

	@ProtocolEntityCallback("success")
	def onSuccess(self, successProtocolEntity):
		print "----- CONECTADO ----- \n"
		entity = AvailablePresenceProtocolEntity()
		self.toLower(entity)

	@ProtocolEntityCallback("ack")
	def onAck(self, entity):
		if entity.getClass() == "message":
			print "Enviado"

 		
	@ProtocolEntityCallback("receipt")
	def onReceipt(self, entity):
		self.toLower(entity.ack())            

	@ProtocolEntityCallback("message")
	def onMessage(self, messageProtocolEntity):
		print "--Mensagem recebida  \n"
		if messageProtocolEntity.getType()	== 'text':
			# pega mensagem recebida e 
			# numero do remetente
			msg = messageProtocolEntity.getBody()
			remetente = messageProtocolEntity.getFrom()

			# verifica no controlador se ja foi iniciada uma
			# conversa com o remetente
			if remetente in self.conv_with:
				# se ja tiver iniciado
				# pega o estado da conversa
				current_stage = self.conv_stage[remetente]	
				
				# responde de acordo com o estagio da conversa
				# e modifica o controlador
				if current_stage == 1:
					outMsg = TextMessageProtocolEntity(
						self.resp[current_stage] ,
						to = remetente
					)
					self.toLower(outMsg)

					self.conv_stage[remetente] = 2
				elif current_stage 	== 2:
					outMsg = TextMessageProtocolEntity(
						self.resp[current_stage] ,
						to = remetente
					)
					self.toLower(outMsg)

					self.conv_stage[remetente] = 3
				elif current_stage == 3:
					outMsg = TextMessageProtocolEntity(
						self.resp[current_stage] ,
						to = remetente
					)
					self.toLower(outMsg)	

					self.conv_stage[remetente] = 4
				elif current_stage == 4:
					outMsg = TextMessageProtocolEntity(
						self.resp[current_stage] ,
						to = remetente
					)
					self.toLower(outMsg)	
			else:
				# se nao, envia a primeira mensagem
				outMsg = TextMessageProtocolEntity(
					self.resp[0] ,
					to = remetente
				)
				self.toLower(outMsg)

				# salva os dados da conversa no controlador
				self.conv_with.append(remetente)
				self.conv_stage[remetente] = 1

