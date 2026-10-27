#!/usr/bin/env python3
"""Synchronize individually selected Actions Secrets with GitHub OIDC."""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request


def selected_secret(name, value, allowed):
    if name.upper().startswith('GITHUB_') or name not in allowed:
        raise ValueError('Secret name is not selected by this project')
    if not value:
        raise ValueError('Configure the repository Actions Secret: ' + name)
    return {'name': name, 'value': value}


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


def outputs(names):
    if os.environ.get('GITHUB_OUTPUT'):
        with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
            output.write('names=' + json.dumps(names) + '\nhas_secrets=' + str(bool(names)).lower() + '\n')


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else 'config'
    base = os.environ.get('VPS_SECRETS_ENDPOINT', 'https://viniciusnunes.dev.br/.well-known/vps-secrets').rstrip('/')
    if not base.startswith('https://'):
        raise SystemExit('Secret synchronization requires HTTPS')
    for attempt in range(10):
        try:
            token = oidc(base)
            if mode == 'status':
                print(json.dumps(call(base + '/status', 'GET', token), indent=2))
                return
            config = call(base + '/config', 'GET', token)
            names = config['secretNames']
            if any(name.upper().startswith('GITHUB_') for name in names):
                raise ValueError('Reserved GitHub credentials cannot be synchronized')
            if mode == 'config':
                outputs(names)
                if not names:
                    call(base + '/secrets', 'POST', token, {'secrets': {}})
                print('Selected Secret names: ' + ', '.join(names))
                return
            if mode == 'finalize':
                result = call(base + '/finalize', 'POST', token, {})
            else:
                item = selected_secret(os.environ['VPS_SECRET_NAME'], os.environ['VPS_SECRET_VALUE'], names)
                if mode == 'sync-single':
                    if names != [item['name']]:
                        raise ValueError('This workflow supports exactly one selected Secret')
                    result = call(base + '/secrets', 'POST', token, {'secrets': {item['name']: item['value']}})
                elif mode == 'stage':
                    result = call(base + '/secret', 'POST', token, item)
                else:
                    raise ValueError('Unsupported synchronization command')
            print('Secret synchronization completed for ' + result['project'])
            return
        except urllib.error.HTTPError as error:
            if error.code == 404 and mode == 'config':
                outputs([])
                print('Repository not registered yet. Commit its project file in vps-infra; the platform will start it automatically.')
                return
            if error.code == 409:
                details = json.loads(error.read()).get('error', '')
                if details.startswith('A newer workflow'):
                    print('Synchronization skipped: a newer workflow already applied this state.')
                    return
            if error.code not in {404, 429, 500, 502, 503, 504}:
                raise SystemExit(f'Secret synchronization returned HTTP {error.code}; check the configured names and workflow identity.')
        except ValueError as error:
            raise SystemExit(str(error))
        except (urllib.error.URLError, TimeoutError):
            pass
        if attempt < 9:
            time.sleep(min(2 ** attempt, 15))
    raise SystemExit('Secret synchronization is temporarily unavailable; the platform will retry automatically.')


if __name__ == '__main__':
    main()
