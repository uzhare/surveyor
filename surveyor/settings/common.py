import os
here = lambda * x: os.path.abspath(os.path.join(os.path.abspath(__file__), *x))
PROJECT_ROOT = here('..', '..', '..')
root = lambda * x: os.path.join(os.path.abspath(PROJECT_ROOT), *x)
