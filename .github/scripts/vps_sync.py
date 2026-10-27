#!/usr/bin/env python3
"""Send only explicitly mapped repository Secrets, using a short-lived OIDC token."""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def select_secrets(context, names):
    normalized = {key.upper(): value for key, value in context.items()}
    if any(name.startswith('GITHUB_') for name in names):
        raise ValueError('Reserved GitHub credentials cannot be synchronized')
    missing = sorted(set(names) - set(normalized))
    if missing:
        raise ValueError('Configure these repository Actions Secrets: ' + ', '.join(missing))
    return {name: normalized[name] for name in names}


def oidc(audience):
    url = os.environ['ACTIONS_ID_TOKEN_REQUEST_URL']
    separator = '&' if '?' in url else '?'
    req = urllib.request.Request(url + separator + urllib.parse.urlencode({'audience': audience}),
        headers={'Authorization': 'Bearer ' + os.environ['ACTIONS_ID_TOKEN_REQUEST_TOKEN']})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)['value']


def call(endpoint, method, token, payload=None):
    req = urllib.request.Request(endpoint, method=method,
        data=None if payload is None else json.dumps(payload).encode(),
        headers={'Authorization': 'Bearer ' + token, 'Content-Type': 'application/json',
                 'User-Agent': 'vps-infra/1.0 (+https://github.com/ViniciusRossmann/vps-infra)'})
    with urllib.request.urlopen(req, timeout=30) as response:
        return json.load(response)


def main():
    base = os.environ.get('VPS_SECRETS_ENDPOINT', 'https://viniciusnunes.dev.br/.well-known/vps-secrets').rstrip('/')
    if not base.startswith('https://'):
        raise SystemExit('Secret synchronization requires HTTPS')
    context = json.loads(os.environ.get('VPS_REPOSITORY_SECRETS', '{}'))
    for attempt in range(10):
        try:
            token = oidc(base)
            if len(sys.argv) > 1 and sys.argv[1] == 'status':
                print(json.dumps(call(base + '/status', 'GET', token), indent=2))
                return
            config = call(base + '/config', 'GET', token)
            selected = select_secrets(context, config['secretNames'])
            result = call(base + '/secrets', 'POST', token, {'secrets': selected})
            print(f'Secrets synchronized for {result["project"]}; values_changed={result["changed"]}')
            return
        except urllib.error.HTTPError as error:
            if error.code == 404:
                print('Repository not registered yet. Commit its project file in vps-infra; the platform will start it automatically.')
                return
            if error.code == 409:
                details = json.loads(error.read()).get('error', '')
                if details.startswith('A newer workflow'):
                    print('Synchronization skipped: a newer workflow already applied this state.')
                    return
                raise SystemExit('Secret synchronization conflicted with an externally managed Secret; inspect the application configuration.')
            if error.code not in {429, 500, 502, 503, 504}:
                raise SystemExit(f'Secret synchronization returned HTTP {error.code}; check the configured names and workflow identity.')
        except ValueError as error:
            # This error only lists missing names, never the context or its values.
            raise SystemExit(str(error))
        except (urllib.error.URLError, TimeoutError):
            pass
        if attempt < 9:
            time.sleep(min(2 ** attempt, 15))
    raise SystemExit('Secret synchronization is temporarily unavailable; the platform will retry automatically.')


if __name__ == '__main__':
    main()
