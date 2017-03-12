from urlparse import urlparse, urljoin

from workflow import web


def is_valid_jenkins_url(url):
    parsed = urlparse(url)
    if not all([
        parsed.netloc,
        parsed.scheme,
    ]):
        return False

    return True


def get_jobs(url):
    api_url = urljoin(url, 'api/json')
    r = web.get(api_url)
    r.raise_for_status()
    return r.json()['jobs']