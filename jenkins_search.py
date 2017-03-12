#!/usr/bin/env python
from functools import partial
import sys
from urlparse import urljoin, urlparse

from workflow import Workflow3, web


def main(wf):
    for base_url in wf.settings['jenkinses']:
        query = wf.args[0].lower()
        parsed_url = urlparse(base_url)
        cache_key = parsed_url.netloc.replace('.', '_').replace(':', '-')
        api_url = urljoin(base_url, 'api/json')
        fetcher = partial(fetch_jobs, api_url)
        jobs = wf.cached_data(cache_key, fetcher, max_age=5 * 60) or []

        for job in jobs:
            if query not in job['name'].lower():
                continue

            job_url = urljoin(base_url, 'job/{}/'.format(job['name']))
            wf.add_item(
                title=job['name'],
                subtitle=parsed_url.netloc,
                arg=job_url,
                valid=True,
            )

    wf.send_feedback()


def fetch_jobs(api_url):
    r = web.get(api_url)
    r.raise_for_status()
    return r.json()['jobs']


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))
