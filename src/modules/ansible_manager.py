import os
import time

class AnsibleManager:
    def __init__(self, ssh_connection, playbook_dir="/etc/ansible/playbooks", debug=False):
        self.debug = debug
        self.ssh_connection = ssh_connection 
        self.playbook_dir= "/etc/ansible/playbooks/"
        self.inventory_file = "/etc/ansible/hosts"
        self.private_key_file = "~/.ssh/remote-operator-keys"
        self._create_remote_directory(self.playbook_dir)


    def _create_remote_directory(self, directory):
        """Create a directory on the remote server."""
        command = f'mkdir -p {directory}'
        self.ssh_connection.execute_command(command)


    def config_host_key_checking(self):
        """Configure host key checking on the remote server."""
        
        config_content = f"""
[defaults]
inventory = /etc/ansible/hosts
host_key_checking = False

[ssh_connection]
ssh_args = -o StrictHostKeyChecking=no
        """
        command = f"echo '{config_content}' >> /etc/ansible/ansible.cfg"

        stdout, stderr = self.ssh_connection.execute_command(command)

        if stderr:
            print(f"Error configuring host key checking: '{command}' : {stderr}")
        else:
            print(f"Success Configuring host key checking")


    def setup_ansible(self):
        """Set up Ansibles and its dependencies on the remote server."""
        commands = [
            "sudo apt-get update",
            "sudo apt-get install -y software-properties-common",
            "sudo apt-add-repository --yes --update ppa:ansible/ansible",
            "sudo apt-get install -y ansible"
        ]

        for command in commands:
            stdout, stderr = self.ssh_connection.execute_command(command)
            
            if self.debug:
                if stderr:
                    print(f"Error executing command '{command}' : {stderr}")
                else:
                    print(f"Output of command '{command}': {stdout}")

        self.config_host_key_checking()

        stdout, stderr = self.ssh_connection.execute_command("ansible --version")
        if "ansible" in stdout:
            print("Success installing Ansible")
        else:
            print("Error installing Ansible")


    def register_private_key(self, private_key_file):
        """Register the private key on the server."""
        with open(private_key_file, 'r') as file:
            private_key = file.read()

        commands = [f"echo '{private_key}' | sudo tee -a {self.private_key_file}",
                    f"sudo chmod 600 {self.private_key_file}"]
        
        for command in commands:
            stdout, stderr = self.ssh_connection.execute_command(command)
            
            if self.debug:
                if stderr:
                    print(f"Error executing command '{command}' : {stderr}")
                else:
                    print(f"Output of command '{command}': {stdout}")

        print("Private key registered successfully")

    def create_playbook(self, playbook_name, content):
        """Create an Ansible playblook on the remote server."""
        playbook_path = os.path.join(self.playbook_dir, playbook_name)
        command = f"echo '{content}' > {playbook_path}"
        stdout, stderr = self.ssh_connection.execute_command(command)
        if stderr:
            print(f"Error creating playbook '{playbook_name}' : {stderr}")
        else:
            print(f"Playbook '{playbook_name}' created at {playbook_path}")


    def run_playbook(self, playbook_name, group=None):
        """Run an Ansible playbook on the remote server, optionally targeting a specific group."""
        playbook_path = os.path.join(self.playbook_dir, playbook_name)
        if group:
            command = f"ansible-playbook {playbook_path} -l {group} --private-key {self.private_key_file}"
        else:
            command = f"ansible-playbook {playbook_path} --private-key {self.private_key_file}"

        stdout, stderr = self.ssh_connection.execute_command(command)
        
        if stderr:
            print(f"Error running playbook '{playbook_name}: {stderr}'")
        else:
            print(f"Output of playbook '{playbook_name}: {stdout}'")

        
    def check_playbook_execution(self, playbook_name):
        """Check the execution status of an Ansible playbook on the remote server"""
        
        playbook_path = os.path.join(self.playbook_dir, playbook_name)
        command = f"ansible-playbook --status=check {playbook_path}"
        stdout, stderr = self.ssh_connection.execute_command(command)
        if stderr:
            print(f"Error checking playbook '{playbook_name}': {stderr}")
        else:
            print(f"Output of playbook '{playbook_name}': {stdout}")
    

    def get_playbook_output(self, playbook_name):
        """Retrieve the output of a playbook execution on the remote server"""

        playbook_path = os.path.join(self.playbook_dir, playbook_name)
        command = f"ansible-playbook --status=check {playbook_path}"
        stdout, stderr = self.ssh_connection.execute_command(command)
        if stderr:
            print(f"Error retrieving output for playbook '{playbook_name}': {stderr}")
        else:
            return stdout
    

    def register_hosts(self, hosts_input, group):
        if isinstance(hosts_input, str): # Assume it's a file path
            with open(hosts_input, 'r') as file:
                hosts = file.readlines()
        elif isinstance(hosts_input, list): # Assume it's a list of hosts
            hosts = hosts
        else:
            raise ValueError("Input must be either a file path or a list of hosts")
        hosts = [host.strip() for host in hosts if host.strip()]
        inventory_content = f"[{group}]\n" + "\n".join(hosts)
        stdout, stderr = self.ssh_connection.execute_command(f"echo '{inventory_content}' | sudo tee -a {self.inventory_file}")
        if stderr:
            print(f"Error registering hosts: {stderr}")
        else:
            print(f"Hosts registered successfully: {stdout}")

    def retrieve_inventory(self):
        stdout, stderr = self.ssh_connection.execute_command(f"cat {self.inventory_file}")
        if stderr:
            print(f"Error retrieving inventory: {stderr}")
        else:
            return stdout
