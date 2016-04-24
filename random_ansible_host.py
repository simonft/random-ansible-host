#!/usr/bin/python2.7

from ansible.inventory import Inventory
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.errors import AnsibleError

import getpass
import sys
import os
import click
import random

@click.group()
@click.option('--inventory', default='', help="Path to inventory")
@click.pass_context
def cli(ctx, inventory):
    ctx.obj={}
    ctx.obj['inventory'] = inventory

@cli.command()
def list_groups():
    """list all groups"""
    inventory = setup_inventory()    
    print ""
    print "Possible Groups:"
    for group in inventory.list_groups():
        print '    {}'.format(group)

@cli.command()
@click.argument('group')
def list_hosts(group):
    """lists the hosts in a group"""
    inventory = setup_inventory()
    print ""
    for host in inventory.list_hosts(group):
        print '    {}'.format(host)

@cli.command()
@click.argument('group')
@click.option('--username', envvar='USERNAME', default='', help="username for ssh")
@click.option('--ssh-key', '-i', default='', help="key for ssh")
def ssh(group, username, ssh_key):
    """ssh to a random host in the group"""
    inventory = setup_inventory()
    if username:
        username = '{}@'.format(username)
    ssh_options = ''
    if ssh_key:
        ssh_options = '{}{}'.format(ssh_options, '-i ssh_key')
   
    os.system('ssh {}{}'.format(username, random.choice(inventory.list_hosts(group))))


@click.pass_context
def setup_inventory(ctx):
    loader = DataLoader()
    variable_manager = VariableManager()

    try:
        if(ctx.obj['inventory']):
            return Inventory(loader=loader,
                             variable_manager=variable_manager,
                             host_list=ctx.obj['inventory'])
        else:
            return Inventory(loader=loader,
                             variable_manager=variable_manager)
            
    except AnsibleError as e:
        if str(e) == 'Decryption failed':
            vault_password = getpass.getpass('Enter vault password:')
            loader.set_vault_password(vault_password)

            if(ctx.obj['inventory']):
                return Inventory(loader=loader,
                                 variable_manager=variable_manager,
                                 host_list=ctx.obj['inventory'])
            else:
                return Inventory(loader=loader,
                                 variable_manager=variable_manager)
        else:
            print "Something went wrong:"
            print repr(e)
            sys.exit(1)
