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


import os
import re

class PropLoader:
    """Class responsible for loading SheerID properties file for API interaction"""

    @classmethod
    def load_props(cls, name):
        filename = "{0}/.sheerid.d/{1}".format(os.environ.get("HOME"), name)
        if not os.path.isfile(filename):
            return None
        with open(filename, "rU") as propFile:
            propDict = dict()
            for propLine in propFile:
                if propLine[0] == '#':
                    continue
                parts = propLine.split('=', 1)
                if len(parts) == 2:
                    name = parts[0].strip()
                    value = parts[1].strip()
                    propDict[name] = value
            return propDict

    @classmethod
    def load_props_file(cls):
        with open(os.environ.get("HOME") + "/.sheerid", "rU") as propFile:
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
