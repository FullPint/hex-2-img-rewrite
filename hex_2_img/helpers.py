# Standard Library Imports
from glob import glob
import os
import re

# Package Imprts
from toolz.itertoolz import partition_all

# User Defined Imports

# User Defined VARS
DEFAULT_WIDTHS = {
    9: 32,
    29: 64,
    59: 128,
    99: 256,
    199: 384,
    499: 512,
    999: 768,
    1024: 1024,
}
