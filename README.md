# random-ansible-host

SSH into a random host in a given Ansible group. Useful for when you
just need to get onto one host in a group, and don't care which.

Usage:
```
rah --inventory PATH_TO_INVENTORY_FILE_OR_DIRECTORY ssh ANSIBLE_GROUP
```