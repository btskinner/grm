#!/usr/bin/env python3

import pexpect

pexpect.run('gitroom', withexitstatus = True, events={'CHOICE: ': '9'})
