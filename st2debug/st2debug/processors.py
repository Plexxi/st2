# Licensed to the StackStorm, Inc ('StackStorm') under one or more
# contributor license agreements.  See the NOTICE file distributed with
# this work for additional information regarding copyright ownership.
# The ASF licenses this file to You under the Apache License, Version 2.0
# (the "License"); you may not use this file except in compliance with
# the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os

from six.moves.configparser import ConfigParser

__all__ = [
    'process_st2_config',
    'process_mistral_config',
    'process_content_pack_dir'
]

# Options which should be removed from the st2 config
ST2_CONF_OPTIONS_TO_REMOVE = {
    'database': ['username', 'password'],
    'messaging': ['url']
}


# Options which should be removed from the st2 config
MISTRAL_CONF_OPTIONS_TO_REMOVE = {
    'database': ['connection']
}

REMOVED_VALUE_NAME = '**removed**'



def process_st2_config(config_path, tmp_prefix):
    """
    Remove sensitive data (credentials) from the StackStorm config.

    :param config_path: Full absolute path to the st2 config inside TMP_DIR.
    :type config_path: ``str``
    :param tmp_prefix: Base path where temporary files are placed.
    :type tmp_prefix: ``str``
    """
    assert config_path.startswith(tmp_prefix)

    if not os.path.isfile(config_path):
        return

    config = ConfigParser()
    config.read(config_path)

    for section, options in ST2_CONF_OPTIONS_TO_REMOVE.items():
        for option in options:
            if config.has_option(section, option):
                config.set(section, option, REMOVED_VALUE_NAME)

    with open(config_path, 'w') as fp:
        config.write(fp)


def process_mistral_config(config_path, tmp_prefix):
    """
    Remove sensitive data (credentials) from the Mistral config.

    :param config_path: Full absolute path to the mistral config inside TMP_DIR.
    :type config_path: ``str``
    :param tmp_prefix: Base path where temporary files are placed.
    :type tmp_prefix: ``str``
    """
    assert config_path.startswith(tmp_prefix)

    if not os.path.isfile(config_path):
        return

    config = ConfigParser()
    config.read(config_path)

    for section, options in MISTRAL_CONF_OPTIONS_TO_REMOVE.items():
        for option in options:
            if config.has_option(section, option):
                config.set(section, option, REMOVED_VALUE_NAME)

    with open(config_path, 'w') as fp:
        config.write(fp)


def process_content_pack_dir(pack_dir, tmp_prefix):
    """
    Remove config.yaml from the pack directory.

    :param pack_dir: Full absolute path to the pack directory inside TMP_DIR.
    :type pack_dir: ``str``
    :param tmp_prefix: Base path where temporary files are placed.
    :type tmp_prefix: ``str``
    """
    assert pack_dir.startswith(tmp_prefix)

    config_file_path = os.path.join(pack_dir, 'config.yaml')
    if os.path.isfile(config_file_path):
        os.remove(config_file_path)
