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


"""Demonstrate some basic functionality of the SheerID verification API."""
from sheerid import SheerID
import json
from operator import itemgetter

def demonstrate(key):
    api = SheerID(key, verbose=True)

    response = api.get('/ping')
    print 'Expected response "pong":', response

    response = api.get('/organizationType')
    print 'Org Types:', str(response)

    response = api.post('/verification', params={"FIRST_NAME":"Test","LAST_NAME":"User","SSN_LAST4":"1234"})
    r_obj = json.loads(response)
    print 'Verification response:', r_obj['result']

    response = api.listOrganizations(name='Reserve',type="MILITARY")
    orgs = ', '.join(map(itemgetter('name'), response))
    print 'Reserve Military Organizations:', orgs


if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print "Please provide a valid API key for your account"
        print "Usage: python demo.py <API_KEY>"
        sys.exit(1)
    key = sys.argv[1]
    demonstrate(key)