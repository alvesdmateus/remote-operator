import argparse
import os 
import paramiko
from modules import ansible_manager, ssh_connection

def setup_ansible(ssh_conn):
    ansible_client = ansible_manager.AnsibleManager(ssh_conn)
    #Check if Ansible is already installed
    stdout, stderr = ssh_conn.execute_command("ansible --version")
    if "ansible" in stdout:
        print("Ansible is already installed")
    else:
        ansible_client.setup_ansible()
    
def register_hosts_in_inventory(ssh_conn, hosts_input, group="all"):
    ansible_client = ansible_manager.AnsibleManager(ssh_conn)
    ansible_client.register_hosts(hosts_input, group)

def register_private_key(ssh_conn, private_key):
    ansible_client = ansible_manager.AnsibleManager(ssh_conn)
    ansible_client.register_private_key(private_key)


def create_playbook(ssh_conn, playbook_name, content):
    ansible_client = ansible_manager.AnsibleManager(ssh_conn)
    if os.path.isfile(content):
        with open(content, "r") as file:
            content = file.read()
            
    ansible_client.create_playbook(playbook_name, content)

def run_playbook(ssh_conn, playbook_name, group="all"):
    ansible_client = ansible_manager.AnsibleManager(ssh_conn)
    ansible_client.run_playbook(playbook_name,  group, )


def main():
    hostname="localhost"
    port=2222
    username="root"
    password="test123"
    parser = argparse.ArgumentParser(description="Remote Operator CLI")
    
    subparsers = parser.add_subparsers(dest="command")
    
    setup_parser = subparsers.add_parser("setup", help="Setup Ansible on the remote server")

    key_parser = subparsers.add_parser("key", help="Register the private key.")
    key_parser.add_argument("--key-path", type=str, help="Path to the private key file.")
    

    register_parser = subparsers.add_parser("register", help="Register hosts in the inventory")
    register_parser.add_argument("--hosts-input", help="Path to the hosts file or list of hosts")
    register_parser.add_argument("--group", default="all", help="Group to register the hosts in (default: 'all')")

    create_parser = subparsers.add_parser("create", help="Create an Ansible playbook on the remote server")
    create_parser.add_argument("playbook_name", help="Name of the playbook")
    create_parser.add_argument("content", help="Path to the playbook content, or a YAML string itself")
    
    run_parser = subparsers.add_parser("run", help="Run an Ansible playbook on the remote server")
    run_parser.add_argument("playbook_name", help="Name of the playbook")
    run_parser.add_argument("group", default="all", help="Group to run the playbook on")
    args = parser.parse_args()
    
   
    
    ssh_conn = ssh_connection.SSHConnection(hostname=hostname, port=port, username=username, password=password)
    ssh_conn.connect()

    if args.command == "setup":
        setup_ansible(ssh_conn)
    if args.command == "key":
        register_private_key(ssh_conn, args.key_path)
    elif args.command == "register":
        register_hosts_in_inventory(ssh_conn, args.hosts_input, args.group)
    elif args.command == "create":
        create_playbook(ssh_conn, args.playbook_name, args.content)
    elif args.command == "run":
        run_playbook(ssh_conn, args.playbook_name, args.group)

    ssh_conn.close()

if __name__ == "__main__":
    main()

