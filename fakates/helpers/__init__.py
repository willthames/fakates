# Copyright: (c) 2018, Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from copy import deepcopy


def dict_merge(a, b, remove_nulls=False):
    '''recursively merges dicts. not just simple a['key'] = b['key'], if
    both a and b have a key whose value is a dict then dict_merge is called
    on both values and the result stored in the returned dictionary.
    Removes keys with null values
    '''
    if not isinstance(b, dict):
        return b
    result = deepcopy(a)
    for k, v in b.items():
        if k in result and isinstance(result[k], dict):
            result[k] = dict_merge(result[k], v)
            if result[k] is None and remove_nulls:
                del result[k]
        else:
            if not remove_nulls or result[k] is not None:
                result[k] = deepcopy(v)
    return result
