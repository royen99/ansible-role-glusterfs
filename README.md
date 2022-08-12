# Ansible Role Glusterfs

[![Build Status](https://dev.azure.com/INGCDaaS/IngOne/_apis/build/status/P12647/P12647-ansible-role-glusterfs?repoName=PP12647-ansible-role-glusterfs&branchName=master)](https://dev.azure.com/INGCDaaS/IngOne/_build/latest?definitionId=26331&repoName=P12647-ansible-role-glusterfs&branchName=master)

Role to install GlusterFS on the target systems

## Requirements

Ansible inventory must contain three (3) RHEL nodes within the same Private Network (or at least be able to communicate freely)

## Role Variables

There are a few default variables that can be changed:

| Variable | Default | Description |
| :---: | :---: | :---: |
| disk_type | Virtual disk | Type of disk from virtualization layer or direct link |
| glusterfs_vgname | gfsvg | VG name to be used for GlusterFS volumes. |
| glusterfs_poolname | gfspool | LV thinpool name for GlusterFS |
| glusterfs_vgsize | 15 | VG size in GiB |
| glusterfs_replicas | 3 | Fixed set of nodes to be online to allow changes to the file system.|
| glusterfs_defaultvolumesize | 1 | GlusterFS volume size in GiB |
| glusterfs_serveroptions | `see below example` | json list of advanced options |

```yaml
  glusterfs_serveroptions:
    {cluster.enable-shared-storage: enable, }
```

This role makes use of the gluster tree. For example:

```yaml
  vars:
    gluster:
      volumes:
        - name: volume1                               # Name of a gluster-volume
          size: 10                                    # Wanted (total) size of the volume in GB
          options:                                    # json list of desired volume options
            { performance.cache-refresh-timeout: '9',
              performance.cache-size: 128MB,
              cluster.server-quorum-type: 'server',
              write-behind: 'off',
              quick-read: 'on'
            }
          snapshot:
            state: on                                 # If a scheduled gluster snapshot should be taken (requires also hour and keep)
            hour: 12                                  # Time (in 24h) when a daily snapshot needs to take place
            keep: 7                                   # Amount of previous snapshots to keep
```

Multiple volumes (and each with different options) can be specified. When volumes already exist, options can be altered.
To for instance extend a volume that was created with 10GB, set its `size:` var to the new desired value and rerun the ansible job.

| Variable | Required | Choices| Description |
| :--- | :---: | :---: | :---: |
| volumes | no | | A list of dictionaries that contain volumes that should be created/removed. |

### Volume

The volume dictionary has the following variables:

| Variable | Required | Choices| Description |
| :--- | :---: | :---: | :---: |
| name | yes | | The name of the volume |
| size | no | Size in GiB | Size of the volume (Required during creation) |
| options | no | | A json containing the gluster options to be used |
| acl | no | | A list of dictionaries containing hosts that should have access to the volumes |
| snapshot | no | | A dictionary of settings for the snapshot functionality |

### snapshot

| Variable | Required | Choices| Description |
| :--- | :---: | :---: | :---: |
| state | yes | <enable/disable> | State to set the snapshot functionality to |
| hour | no | <1-24> | Time snapshot should be taken. Required for `state=on`
| keep | no | <1-99> | Amount of previous snapshots to keep. Required for `state=on`

## Dependencies

There are no dependencies for this role.  For running on IPC RHEL VM's it would however be recommended to make use of a ansible-role for detect-become-method for running on IAMaaS enabled nodes.

## Example Playbook

Including an example of how to use your role (for instance, with variables passed in as parameters) is always nice for users too:

```yaml
---

- name: GlusterFS
  hosts: all
  become: true
  strategy: linear
  gather_facts: false
  vars:
    gluster:
      volumes:
        - name: volume1
          size: 30
          options:
            { performance.cache-refresh-timeout: '9',
              performance.cache-size: 128MB,
              cluster.server-quorum-type: 'server',
              write-behind: 'off',
              quick-read: 'on'
            }
          snapshot:
            state: on
            hour: 12
            keep: 7
        - name: volume2
          size: 30
          options:
            { performance.cache-refresh-timeout: '9',
              performance.cache-size: 128MB,
              cluster.server-quorum-type: 'server',
              write-behind: 'off',
              quick-read: 'on'
            }
          snapshot:
            state: on
            hour: 11
            keep: 9

  pre_tasks:
    - name: Run ansible-role-detect-become-method
      include_role:
        name: ansible-role-detect-become-method

  roles:
    - ansible-role-glusterfs

```

## Author Information

[Linux Squad](mailto:teamlinux@ing.com)