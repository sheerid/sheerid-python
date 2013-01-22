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

DEFAULT_CHUNK = 500

class SheerID:
    """API Wrapper for accessing SheerID's RESTful interface."""

    def __init__(self, access_token, base_url=SHEERID_ENDPOINT_SANDBOX,
                 target_version="0.5", verbose=False):
        """Create an API access object using an API access token.
        Can also specifiy a different endpoint such as production,
        or a different version if necessary."""
        self.access_token = access_token
        self.base_url = base_url
        self.verbose = verbose
        self.target_version = target_version

    def issueToken(self, request_id):
        """Issue a token to facilitate an Asset upload via Upload."""
        json_object = self.post_json("/asset/token", {"requestId":request_id})
        return json_object.token

    def listAffiliationType(self):
        """Obtain a list of affiliation types, optionally filtered by organization type."""
        return self.get_json('/affiliationType')

    def listAssetTypes(self):
        """Obtain a list of asset types."""
        return self.get_json('/assetType')

    def listFields(self):
        """Obtain a list of fields which can be supplied as inputs to Verify."""
        return self.get_json('/field')

    def listOrganizations(self, name='', type=''):
        """List organizations, optionally filtered by type."""
        return self.get_json('/organization', {'name':name, 'type':type})

    def listOrganizationTypes(self):
        """Obtain a list of organization types."""
        return self.get_json('/organizationType')

    def listVerificationTypes(self):
        """Obtain a list of verification types."""
        return self.get_json('/verificationType')

    def listRewardPools(self):
        """Obtain a list of reward pools."""
        return self.get_json('/rewardPool')

    def retrieveRewardPool(self, rewardPoolId):
        """Retrieve a reward pool by id."""
        return self.get_json('/rewardPool/%s' % str(rewardPoolId))

    def createRewardPool(self, name, data, warnThreshold=None):
        """Create a reward pool with initial reward data."""
        pools = self.listRewardPools()
        if name in [x['name'] for x in pools]:
            for pool in pools:
                if pool['name'] == name:
                    _id = pool['id']
        else:
            param = {'name':name}
            if warnThreshold:
                param['warnThreshold'] = warnThreshold
            resp = self.post_json('/rewardPool', param)
            _id = resp['id']
        self.addEntries(_id, data)
        return _id

    def addEntries(self, rewardPoolId, data):
        """Add one or more entries to a reward pool."""
        resource = '/rewardPool/%s' % str(rewardPoolId)
        for d in [data[i:i+DEFAULT_CHUNK]
                  for i in range(0, len(data), DEFAULT_CHUNK)]:
            param = [('entry', x,) for x in d]
            self.post(resource, param)

    def listRewards(self):
        """Obtain a list of existing rewards."""
        return self.get_json('/reward')

    def retrieveReward(self, rewardId):
        """Retrieve a reward by its id."""
        return self.get_json('/reward/%s' % str(rewardId))

    def createUnpooledReward(self, name, rewardCode, product_key_name, instructions=None):
        """Create a single reward to be distributed upon successful
        verification."""
        param = {"name": name, product_key_name: rewardCode}
        if instructions:
            param["instructions"] = instructions
        self.post_json('/reward', param)

    def createPooledReward(self, name, rewardPoolId, product_key_name, instructions=None):
        """Create a reward to be distributed upon successful verification,
        drawn from the specified pool."""
        param = {"name": name, product_key_name: 'pooled:%s'%rewardPoolId}
        if instructions:
            param["instructions"] = instructions
        self.post_json('/reward', param)

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
        try:
            cfg = cls.load_props()[name]
            return SheerID(cfg['access_token'], cfg['base_url'])
        except KeyError:
            return None

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
