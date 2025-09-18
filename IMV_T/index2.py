import os
import sys
import site

site.addsitedir('C:/Program files/Python36/lib/site-packages')

sys.path.append('/home/pmota/WEB/IMV_T/')
#sys.path.append('/home/xitai/Xitai-W0/webs/xitai_games/xitai_games')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "IMV_T.settings")

activate_env="/home/pmota/WEB/IMV_T/IMV_T_env/bin/activate"
#execfile(activate_env, dict(__file__=activate_env))
#exec(open(activate_env).read(), dict(__file__=activate_env))

from daphne.cli import CommandLineInterface
sys.argv[0] = ''
sys.exit(CommandLineInterface.entrypoint())
