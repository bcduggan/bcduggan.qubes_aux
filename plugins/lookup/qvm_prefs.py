from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: qvm_prefs

short_description: Read preferences for a single qube
description:
  - Read preferences for a single qube

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
  qube:
    description: Target qube
    required: True

author:
  - Brian Duggan <brian@dugga.net>
'''

EXAMPLES = '''
- name: Get current netvm for work qube
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qvm_prefs', 'netvm', qube='work') }}""

- name: Get default netvm for work qube
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qvm_prefs', 'netvm', qube='work', default=True) }}""

- name: List qvm prefs for work qube
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qvm_prefs', 'netvm', qube='work', default=True) }}""
'''
from ansible_collections.bcduggan.qubes_aux.plugins.module_utils.prefs import QvmPrefs
from ansible_collections.bcduggan.qubes_aux.plugins.lookup.qubes_prefs import LookupModule as QubesPrefsLookupModule

class LookupModule(QubesPrefsLookupModule):
  def _prefs(self) -> QvmPrefs:
    return QvmPrefs(self.get_option("qube"))
