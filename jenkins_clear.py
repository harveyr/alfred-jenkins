#!/usr/bin/env python
import sys

from workflow import Workflow3


def main(wf):
    try:
        wf.settings['jenkinses'] = []
        wf.settings.save()
    except Exception:
        wf.logger.exception("Failed to wipe settings")


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
