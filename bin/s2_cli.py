#!/Users/mf840/PycharmProjects/facereco_v1/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 's2protocol==4.11.4.78285.0','console_scripts','s2_cli.py'
__requires__ = 's2protocol==4.11.4.78285.0'
import re
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(
        load_entry_point('s2protocol==4.11.4.78285.0', 'console_scripts', 's2_cli.py')()
    )
