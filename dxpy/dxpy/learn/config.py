from dxpy.configs import ModuleConfigs
from dxpy.filesystem import Path
import os
config = ModuleConfigs('learn', Path(os.environ['HOME']) / '.dxl/dxpy',
                       '.').get_config()
