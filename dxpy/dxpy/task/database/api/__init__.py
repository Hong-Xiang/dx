from .base import create, read, read_all, update, delete, Database
from .cli import main as cli_main
from .web import add_api
from ..config import config
from ..service.base import check_json
from ..exceptions import *
