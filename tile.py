# command line utility to manage tiled windows
from util import *
from manager import *
import sys
from pathlib import Path

# print help thing
def print_usage():
  print('\n'.join([
    'Usage: python3 tile.py [reset | list | close | transpose | focus <direction> | swap <direction>]',
    '  direction = left | right | above | below']))

if __name__ == '__main__':
  # to store the window state
  stash = str(Path.home()) + '/.tiling_configuration'

  def die():
    open(stash, 'w').write(repr(manager))
    exit()

  if len(sys.argv) == 1:
    print_usage()
    exit()
  option = sys.argv[1]

  # force tile all windows & initialize stash
  if option == 'reset':
    manager = Manager.from_reality()
    manager.render()
    die()

  if not Path(stash).is_file():
    print('Error: `{}` does not exist yet\nRun `python3 tile.py reset` first'.format(stash))
    exit()

  with open(stash, 'r') as f:
    manager = Manager.from_str(f.read())

  # list the workspace trees
  if option == 'list':
    print(manager)
    for _, workspace in manager.workspaces.items():
      print(workspace.windows())

  # close focused window
  elif option == 'close':
    manager.close()

  # transpose focused window
  elif option == 'transpose':
    manager.transpose()

  # shift focus
  elif option == 'focus':
    if len(sys.argv) < 3:
      print('Missing direction argument to `focus`')
      die()
    try:
      manager.focus(sys.argv[2])
    except ValueError as e:
      print(e)

  # swap focused window position
  elif option == 'swap':
    if len(sys.argv) < 3:
      print('Missing direction argument to `swap`')
      die()
    try:
      manager.swap(sys.argv[2])
    except ValueError as e:
      print(e)

  else:
    print('Unrecognized option `{}`'.format(option))
    print_usage()

  die() # save changes for next run
