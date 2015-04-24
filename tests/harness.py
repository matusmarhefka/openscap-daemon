#!/usr/bin/python2

# Copyright 2015 Red Hat Inc., Durham, North Carolina.
# All Rights Reserved.
#
# scap-client is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2.1 of the License, or
# (at your option) any later version.
#
# scap-client is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU Lesser General Public License
# along with scap-client.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Martin Preisler <mpreisle@redhat.com>

import scap_client

import tempfile
import shutil
import os.path


def get_template_data_dir():
    # Beware, nasty tricks ahead!
    return os.path.join(
        os.path.dirname(__file__),
        "data_dir_template"
    )


class IntegrationTest(object):
    """Needs a data_dir to work
    """

    def __init__(self, data_dir_path):
        self.data_dir_path = data_dir_path

    def setup_data(self):
        # This ensures that data_dir is prepared and all the directories are in
        # their place. This is necessary so that we can later copy in our test
        # files.

        scap_client.System.prepare_data_dir(self.data_dir_path)

    def copy_to_data(self, template_path):
        """Overrides of setup_data are supposed to use this to copy special
        data files into the temporary data directory.
        """

        shutil.copy(
            os.path.join(get_template_data_dir(), template_path),
            os.path.join(self.data_dir_path, template_path)
        )

    def init_system(self):
        self.system = scap_client.System(self.data_dir_path)

    def teardown_data(self):
        # Most implementations won't do anything here, the entire directory will
        # be recursively removed anyway.
        pass

    def test(self):
        # This is the important method, this is where code is run
        pass

    @classmethod
    def run(cls):
        temp_dir = None

        try:
            temp_dir = tempfile.mkdtemp()
            instance = cls(temp_dir)
            instance.setup_data()
            instance.init_system()
            instance.test()
            instance.teardown_data()

            shutil.rmtree(temp_dir)

        except:
            if temp_dir is not None:
                print(
                    "Examine '%s' to debug failure of this test.\n" % (temp_dir)
                )

            raise