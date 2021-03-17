from context import src # This allows for aunt/uncle imports 

from src.model.model import RubiksModel
from context import src
from src.rubiks.cube import Cube
from src.ui.display_tools import display_console

cube = Cube()
display_console(cube,0)
cube.rotate('R')
display_console(cube,0)
