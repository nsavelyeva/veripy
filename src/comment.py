#!/usr/bin/python3

import os
import sys
import json
import urllib.error
import urllib.request


class Comment:
    def __init__(self, token, tag):
        self.token = token
        self.tag = f'VERIPY_{tag}'
        self.handler = f'<!-- {self.tag} -->'
        self.base_url = self.get_base_url()
        self.pr = self.base_url.split('/')[-2]
        self.headers = {'Accept': 'application/vnd.github.v3+json',
                        'Authorization': f'token {self.token}'}

    def get_base_url(self):
        path = os.getenv('GITHUB_EVENT_PATH')  # /github/workflow/event.json
        with open(path) as json_file:
            payload = json.load(json_file)
        pulls_url = payload['pull_request']['_links']['self']['href']
        if not pulls_url:
            sys.exit('Cannot get "pulls_url" from $GITHUB_EVENT_PATH payload')
        pulls_url += '/reviews'
        return pulls_url  # f'https://api.github.com/repos/{owner}/{repo}/pulls/{self.pr}/reviews'

    def send(self, req, operation):
        try:
            with urllib.request.urlopen(req) as resp:
                status, content = resp.getcode(), resp.read().decode('utf-8')
        except (urllib.error.HTTPError, urllib.error.URLError) as err:
            msg = f'Cannot {operation} comment for the PR #{self.pr} at {self.base_url[:-8]} due to error: {err}'
            print(msg)
            return False, msg
        return True, content

    def find(self):
        num = 0
        req = urllib.request.Request(self.base_url, method='GET', headers=self.headers)
        ok, content = self.send(req, 'find')
        if ok:
            data = json.loads(content)
            for item in data:
                if f'{item["pull_request_url"]}/' in self.base_url and item.get('body', '').startswith(self.handler):
                    num = item['id']
        if num == 0:
            print(f'No comment sent by {self.tag} already exist for the PR #{self.pr} at {self.base_url[:-8]}')
        else:
            print(f'A comment sent by {self.tag} already exists for the PR #{self.pr} at {self.base_url[:-8]}, its id is: {num}')
        return num

    def create(self, body):
        data = {'body': f'{self.handler}\n{body}', 'event': 'COMMENT'}
        data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(self.base_url, method='POST', data=data, headers=self.headers)
        ok, content = self.send(req, 'create')
        if ok:
            print(f'Successfully created a comment for the PR #{self.pr} at {self.base_url[:-8]}')
        else:
            print(f'Failed to create a comment for the PR #{self.pr} at {self.base_url[:-8]} due to error\n{content}')
        return ok, content

    def update(self, body, num):
        data = {'body': f'{self.handler}\n{body}'}
        data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(f'{self.base_url}/{num}', method='PUT', data=data, headers=self.headers)
        ok, content = self.send(req, 'update')
        if ok:
            print(f'Successfully updated comment #{num} for the PR #{self.pr} at {self.base_url[:-8]}')
        else:
            print(f'Failed to update comment #{num} for the PR #{self.pr} at {self.base_url[:-8]} due to error\n{content}')
        return ok, content
