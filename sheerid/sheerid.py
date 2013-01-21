# Copyright 2012 SheerID, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License").
# You may not use this file except in compliance with the License.
# A copy of the License is located at:
#
# http://www.apache.org/licenses/LICENSE-2.0.html
#
# This file is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for
# the specific language governing permissions and limitations under the
# License.
#
# For more information, visit:
#
# http://developer.sheerid.com


import json
from urllib import urlencode
import urllib2
import os

SHEERID_ENDPOINT_SANDBOX = "https://services-sandbox.sheerid.com"

class SheerID:
    """API Wrapper for accessing SheerID's RESTful interface."""

    def __init__(self, access_token, base_url=SHEERID_ENDPOINT_SANDBOX, target_version="0.5", verbose=False):
        self.access_token = access_token
        self.base_url = base_url
        self.verbose = verbose
        self.target_version = target_version

    def get_access_token(self, request_id):
        json_object = self.post_json("/asset/token", {"requestId":request_id})
        return json_object.token

    def listAffiliationType(self):
        return self.get_json('/affiliationType')

    def listAssetTypes(self):
        return self.get_json('/assetType')

    def listFields(self):
        return self.get_json('/field')

    def listOrganizations(self, name='', type=''):
        return self.get_json('/organization', {'name':name, 'type':type})

    def listOrganizationTypes(self):
        return self.get_json('/organizationType')

    def listVerificationTypes(self):
        return self.get_json('/verificationType')

    def get(self, path, params=None):
        req = SheerIDRequest(self.access_token, 'GET', self.url(path), params, self.verbose)
        return req.execute()

    def post(self, path, params=None):
        req = SheerIDRequest(self.access_token, 'POST', self.url(path), params, self.verbose)
        return req.execute()

    def post_json(self, path, params=None):
        return json.loads(self.post(path, params))

    def get_json(self, path, params=None):
        return json.loads(self.get(path, params))

    def url(self, path=''):
        return "%s/rest/%s%s" % (self.base_url, self.target_version, path)

    @classmethod
    def load_props(cls):
        propFile = file( os.environ.get("HOME") + "/.sheerid", "rU" )
        dicts = dict()
        for propLine in propFile:
            if propLine[0] == '[':
                propDict = dict()
                dicts[propLine.strip('[] \n\r')] = propDict
            else:
                parts = propLine.split('=', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    value = parts[1].strip()
                    propDict[name] = value
        propFile.close()
        return dicts

    @classmethod
    def load_instance(cls, name):
        cfg = cls.load_props()[name]
        if cfg:
            return SheerID(cfg['access_token'], cfg['base_url'])

class SheerIDRequest:

    def __init__(self, accessToken, method, url, params=None, verbose=False):
        self.method = method
        self.url = url
        if params:
            self.params = params
        else:
            self.params = dict()
        self.headers = {"Authorization":"Bearer %s" % accessToken}
        self.verbose = verbose

    def execute(self):
        d = urlencode(self.params)
        if self.method == "POST":
            post_data = d
            url = self.url
        else:
            post_data = None
            url = self.url + '?' + d
        if self.verbose:
            print 'URL:', url
            print "Params:", d
        request = urllib2.Request(url, data=post_data, headers=self.headers)
        response = urllib2.urlopen(request)
        return response.read()
