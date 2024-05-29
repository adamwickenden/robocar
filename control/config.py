import os
from pathlib import Path

root = Path(os.sep.join(os.getcwd().split('/')[:-1]))
apps = root / 'Applications'
control = root / 'Applications' / 'control'