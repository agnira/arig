# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

bl_info = {
    "name" : "arig",
    "author" : "Agni Rakai Sahakarya",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Rigging"
}

from . import auto_load

if "auto_load" in locals():
    import importlib
    importlib.reload(auto_load)
    auto_load.init()
    auto_load.reload()

auto_load.init()


def register():
    auto_load.register()
    print('INFO: ' + bl_info['name'] + ' is registered!')

def unregister():
    auto_load.unregister()
    print('INFO: ' + bl_info['name'] + ' is unregistered!')


if __name__ == "__main__":
    register()

