import argparse
import os
import paramiko
from modules import (
    ansible_manager,
    input_manager,
    ssh_connection,
    remote_operator,
)


def main():
    hostname = "localhost"
    port = 2222
    username = "root"
    password = "test123"
    parser = argparse.ArgumentParser(description="Remote Operator CLI")

    subparsers = parser.add_subparsers(dest="command")

    setup_parser = subparsers.add_parser(
        "setup", help="Setup Ansible on the remote server"
    )

    key_parser = subparsers.add_parser("key", help="Register the private key.")
    key_parser.add_argument(
        "--key-path", type=str, help="Path to the private key file."
    )

    register_parser = subparsers.add_parser(
        "register", help="Register hosts in the inventory"
    )
    register_parser.add_argument(
        "--hosts-input", help="Path to the hosts file or list of hosts"
    )
    register_parser.add_argument(
        "--group",
        default="all",
        help="Group to register the hosts in (default: 'all')",
    )

    create_parser = subparsers.add_parser(
        "create", help="Create an Ansible playbook on the remote server"
    )
    create_parser.add_argument("playbook_name", help="Name of the playbook")
    create_parser.add_argument(
        "content", help="Path to the playbook content, or a YAML string itself"
    )

    run_parser = subparsers.add_parser(
        "run", help="Run an Ansible playbook on the remote server"
    )
    run_parser.add_argument("playbook_name", help="Name of the playbook")
    run_parser.add_argument(
        "group", default="all", help="Group to run the playbook on"
    )
    args = parser.parse_args()

    ssh_conn = ssh_connection.SSHConnection(
        hostname=hostname, port=port, username=username, password=password
    )
    ssh_conn.connect()
    ansible_object = ansible_manager.AnsibleManager(ssh_connection=ssh_conn)
    input_object = input_manager.InputManager()

    if args.command == "setup":
        ansible_object.setup_ansible()
    if args.command == "key":
        ansible_object.register_private_key(args.key_path)
    elif args.command == "register":
        ansible_object.register_hosts_in_inventory(args.hosts_input, args.group)
    elif args.command == "create":
        ansible_object.create_playbook(args.playbook_name, args.content)
    elif args.command == "run":
        ansible_object.run_playbook(args.playbook_name, args.group)

    ssh_conn.close()


if __name__ == "__main__":
    main()
