from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: qubes_prefs

short_description: Read global Qubes preferences
description:
  - Read global Qubes preferences

options:
  _terms:
    description:
      - Read value for pref
      - Mutually exclusive with O(list)
    required: False
    type: list
    elements: str
  default:
    description:
      - Read default value for pref
      - Mutually exclusive with O(list)
    required: False
    type: bool
  list:
    description:
      - List pref names
      - Mutually exclusive with O(default)
    required: False
    type: bool

author:
  - Brian Duggan <brian@dugga.net>
'''

EXAMPLES = '''
- name: Get current updatevm
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qubes_prefs', 'updatevm') }}"

- name: Get default updatevm
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qubes_prefs', 'updatevm', default=True) }}"

- name: List Qubes pref names
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qubes_prefs', list=True) }}"
'''
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
from ansible_collections.bcduggan.qubes_aux.plugins.module_utils.prefs import QubesPrefs

type PrefValue = None | bool | str | int | float
type LookupResult = list[str] | list[PrefValue]

display = Display()

class LookupModule(LookupBase):
  def _prefs(self) -> QubesPrefs:
    return QubesPrefs()

  def run(self, terms, variables=None, **kwargs) -> LookupResult:
    self.set_options(var_options=variables, direct=kwargs)
    prefs = self._prefs()
    return (
      prefs.list()
      if self.get_option("list") else (
        [prefs.get_default(term) for term in terms]
        if self.get_option("default") else
        [prefs.get(term) for term in terms]
      )
    )
