from yowsup.common import YowConstants
from yowsup.stacks import  YowStackBuilder
from layer import CreateGroupsLayer
from cadastro_layer import CadastroLayer
from yowsup.layers.auth import AuthError
from yowsup.layers import YowLayerEvent
from yowsup.layers.network import YowNetworkLayer
from yowsup.layers.protocol_messages.protocolentities  import TextMessageProtocolEntity
from yowsup.layers.coder import YowCoderLayer
from yowsup.env import YowsupEnv
from yowsup.layers.axolotl.props import PROP_IDENTITY_AUTOTRUST

class YowsupStack(object):
    def __init__(self, credentials, encryptionEnabled = True):
        stackBuilder = YowStackBuilder()

        self.stack = stackBuilder\
            .pushDefaultLayers(encryptionEnabled)\
            .push(CadastroLayer)\
            .build()

        self.stack.setCredentials(credentials)
        self.stack.setProp(YowNetworkLayer.PROP_ENDPOINT, YowConstants.ENDPOINTS[0]) #whatsapp server address
        self.stack.setProp(YowCoderLayer.PROP_DOMAIN, YowConstants.DOMAIN)
        self.stack.setProp(YowCoderLayer.PROP_RESOURCE, YowsupEnv.getCurrent().getResource()) #info about us as WhatsApp client
        self.stack.setProp(PROP_IDENTITY_AUTOTRUST, True)
        
    def start(self):
        self.stack.broadcastEvent(YowLayerEvent(YowNetworkLayer.EVENT_STATE_CONNECT))
        

        try:
            self.stack.loop()
        except AuthError as e:
            print("Authentication Error: %s" % e.message)
