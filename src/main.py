from modules import ansible_manager, ssh_connection

def install_python_on_hosts(self, hosts_file):
        """Install python on each host listed in the hosts file"""

        with open(hosts_file, "r") as file:
            hosts = file.readlines()
        for host in hosts:
            host = host.strip()
            if not host:
                continue
            print(f"Processing host: {host}")
            ssh_conn = ssh_connection.SSHConnection(
                self.ssh_connection.port,
                self.ssh_connection.username,
                self.ssh_connection.password,
                host
            )
            ssh_conn.connect()
            stdout, stderr = ssh_conn.execute_command("python --version")
            if "python" in stdout:
                print(f"Python is already installed on {host}")
            else:
                print(f"Install Python")
                commands = ["sudo apt update", "sudo apt install -y python3"]
                for command in commands:
                    stdout, stderr = ssh_conn.execute_command(command)
                    if stderr:
                        print(f"Error executing command '{command}' on {host}: {stderr}")
                    else:
                        print(f"Output of command '{command}' on {host}: {stdout}")
            ssh_conn.close()

# Example usage:
if __name__ == '__main__':
    host = "localhost"
    port = 2222
    username = "root"
    password = "test123"
    ssh_conn = ssh_connection.SSHConnection(host, port, username, password)
    ssh_conn.connect()

    ansible_manager = ansible_manager.AnsibleManager(ssh_conn)
    
    # Setup Ansible
    ansible_manager.setup_ansible()

    # Create a sample playbook
    sample_playbook_content = """----
    - hosts: localhost
      tasks:
        - name: Ensure the latest version of git is installed
            apt:
               name: git
               state : latest    
    """
        
    ansible_manager.create_playbook("sample_playbook.yml", sample_playbook_content)
    
    # Run the playbook
    ansible_manager.run_playbook("sample_playbook.yml")
    
    # Check the playbook execution
    ansible_manager.check_playbook_execution("sample_playbook.yml")
    
    ssh_conn.close()