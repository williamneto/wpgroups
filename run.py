import logging
logging.basicConfig(level=logging.DEBUG)
import stack

credentials = ("xxxxxxx", "xxxxx")
stack = stack.YowsupStack(credentials)
stack.start()
