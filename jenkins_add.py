#!/usr/bin/env python
import sys

from workflow import Workflow3
from workflow.notify import notify

import client


def main(wf):
    try:
        url = next(u for u in wf.args if u.startswith('http'))
    except StopIteration:
        url = None

    if not url or not client.is_valid_jenkins_url(url):
        return notify(
            'Jenkins: URL not added',
            '"{}" is not a valid Jenkins URL'.format(url)
        )

    try:
        jenkinses = wf.settings['jenkinses']
    except KeyError:
        jenkinses = []

    try:
        next(u for u in jenkinses if u == url)
        return notify(
            'Jenkins: URL not added',
            '"{}" was already in your list'.format(url)
        )
    except StopIteration:
        pass

    try:
        jobs = client.get_jobs(url)
    except Exception:
        wf.logger.exception("Failed to fetch jobs from %s", url)
        return notify(
            'Jenkins: URL not added',
            'Failed to fetch jobs from "{}"'.format(url)
        )

    wf.logger.info('Adding Jenkins %s', url)
    jenkinses.append(url)

    wf.settings['jenkinses'] = jenkinses
    wf.settings.save()

    notify(
        'Jenkins: URL added!',
        'Found {} jobs.'.format(len(jobs))
    )


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
