#!/usr/bin/env python
import sys

from workflow import Workflow3


def main(wf):
    try:
        jenkinses = wf.settings['jenkinses']
    except KeyError:
        jenkinses = []

    for url in jenkinses:
        wf.add_item(
            title=url,
            arg=url,
            valid=True,
        )

    wf.send_feedback()


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
