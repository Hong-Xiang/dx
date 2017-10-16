import ptvsd

ptvsd.enable_attach("pydebug", address = ('0.0.0.0', 3000))

#ptvsd.wait_for_attach()
