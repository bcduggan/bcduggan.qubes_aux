from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = '''
---
module: qubesdb

short_description: Read qubesdb paths
description:
  - Read qubesdb path values on the local qube

options:
  _terms:
    description:
      - Read data from a path
      - Read multiple values when path ends in '/' (returns dict)
      - Read single value when path does not end in '/' (returns scalar)
    required: True
    type: list
    elements: str
  list:
    description: List paths at path instead of read values at path
    type: bool
    required: False
    default: False

author:
  - Brian Duggan <brian@dugga.net>
'''

EXAMPLES = '''
- name: Get local qube name
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qubesdb', '/name') }}""

- name: List qubes services
  ansible.builtin.debug:
    msg: "{{ lookup('bcduggan.qubes_aux.qubesdb', '/qubes-service', list=True) }}""
'''
from ansible.errors import AnsibleError
from ansible.plugins.lookup import LookupBase
from ansible.utils.display import Display
import qubesdb

type QubesDBValue = None | bool | int | float | str
type QubesDBValues = dict[str, QubesDBValue]
type LookupResult = list[list[str]] | list[QubesDBValue | QubesDBValues]

display = Display()

class LookupModule(LookupBase):
  def __init__(self, *args, **kwargs):
    self.qdb = qubesdb.QubesDB()
    super().__init__(*args, **kwargs)

  def coerce(self, value: bytes) -> QubesDBValue:
      if not value:
          return None
      elif value == b"True":
          return True
      elif value == b"False":
          return False
      else:
          try:
              return int(value)
          except ValueError:
              pass

          try:
              return float(value)
          except ValueError:
              pass

          return value.decode("utf-8")

  def read(self, path: str) -> QubesDBValue | QubesDBValues:
    display.debug(u"Lookup value at path %s from qubesdb" % path)
    try:
      return (
        {
          key: self.coerce(value)
          for key, value in self.qdb.multiread(path).items()
        }

        if path.endswith("/") else

        self.coerce(self.qdb.read(path))
      )
    except qubesdb.Error as exc:
      raise AnsibleError from exc

  def list(self, path: str) -> list[str]:
    display.debug(u"List paths at %s from qubesdb" % path)
    try:
      return self.qdb.list(path)
    except qubesdb.Error as exc:
      raise AnsibleError from exc

  def run(self, terms, variables=None, **kwargs) -> LookupResult:
    self.set_options(var_options=variables, direct=kwargs)
    return (
      [self.list(term) for term in terms]

      if self.get_option("list") else

      [self.read(term) for term in terms]
    )
