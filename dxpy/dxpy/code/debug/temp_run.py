import ptvsd
ptvsd.enable_attach("ptvsd", address = ('0.0.0.0', 3000))

# Enable the line of source code below only if you want the application to wait until the debugger has attached to it
#ptvsd.wait_for_attach()

