# Ansible Collection - bcduggan.qubes

## qubes_policy

The qubes_policy plugin modifies qrexec policies. For example:

```yaml
- name: Write policy
  bcduggan.qubes_aux.qubes_policy:
    name: 30-mgmtvm
    path: 30-mgmtvm

- name: Write include policy
  bcduggan.qubes_aux.qubes_policy:
    name: include/admin-global-ro
    path: include/admin-global-ro

- name: Write templated policy
  bcduggan.qubes_aux.qubes_policy:
    name: 30-split-ssh
    content: "{{ lookup('ansible.builtin.template', './templates/policy/30-split-ssh.j2') }}"

- name: Remove policy
  bcduggan.qubes_aux.qubes_policy:
    name: 35-redundant
    state: absent
```

Where `path` is the path to the the policy under 'files'.

### Admin VMs

Non-dom0 admin VMs can edit policy files when policy allows. To grant an admin VM named `mgmt` the ability to edit policy, add this line to `include/admin-policy-rwx` in dom0:

```
mgmt dom0 allow
```
