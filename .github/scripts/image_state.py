#!/usr/bin/env python3
"""Publish only current main; reuse already published digests on Secret refreshes."""
import base64
import json
import os
import subprocess
import urllib.error
import urllib.parse
import urllib.request


def current_main():
    repository = os.environ['GITHUB_REPOSITORY']
    req = urllib.request.Request(f'https://api.github.com/repos/{repository}/git/ref/heads/main', headers={
        'Authorization': 'Bearer ' + os.environ['GH_TOKEN'], 'Accept': 'application/vnd.github+json',
        'X-GitHub-Api-Version': '2026-03-10'})
    with urllib.request.urlopen(req, timeout=20) as response:
        return json.load(response)['object']['sha'] == os.environ['GITHUB_SHA']


def manifest(repository, reference, token):
    req = urllib.request.Request(f'https://ghcr.io/v2/{repository}/manifests/{reference}', method='HEAD', headers={
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/vnd.oci.image.index.v1+json,application/vnd.docker.distribution.manifest.list.v2+json,application/vnd.oci.image.manifest.v1+json,application/vnd.docker.distribution.manifest.v2+json'})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            return response.headers['Docker-Content-Digest']
    except urllib.error.HTTPError as error:
        if error.code in {401, 403, 404}:
            return None
        raise


def needs_build(repository):
    basic = base64.b64encode((os.environ['GITHUB_ACTOR'] + ':' + os.environ['GH_TOKEN']).encode()).decode()
    query = urllib.parse.urlencode({'service': 'ghcr.io', 'scope': f'repository:{repository}:pull'})
    req = urllib.request.Request('https://ghcr.io/token?' + query, headers={'Authorization': 'Basic ' + basic})
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            token = json.load(response)['token']
    except urllib.error.HTTPError as error:
        if error.code in {401, 403, 404}:
            return True
        raise
    digest = manifest(repository, os.environ['GITHUB_SHA'], token)
    return digest is None or digest != manifest(repository, 'main', token)


def main():
    repository = os.environ['GITHUB_REPOSITORY'].lower()
    if len(os.sys.argv) > 1 and os.sys.argv[1] == 'promote':
        if current_main():
            subprocess.run(['docker', 'buildx', 'imagetools', 'create', '--tag', f'ghcr.io/{repository}:main',
                            f'ghcr.io/{repository}@{os.environ["IMAGE_DIGEST"]}'], check=True)
        else:
            print('Newer main commit found; this build will not replace the deployment channel.')
        return
    current = current_main()
    build = current and needs_build(repository)
    with open(os.environ['GITHUB_OUTPUT'], 'a') as output:
        output.write(f'image=ghcr.io/{repository}\ncurrent={str(current).lower()}\nbuild={str(build).lower()}\n')


if __name__ == '__main__':
    main()
