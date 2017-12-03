from dxpy.configs import ConfigsView
default_config = {
    'backend': 'astra',
    'astra': {
    },
    'projection': dict(),
    'reconstruction': dict()
}
config = ConfigsView(default_config)
