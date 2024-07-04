import paramiko

class SSHConnection:
    def __init__(self, hostname, port, username, password):
        self.hostname = hostname 
        self.port = port
        self.username = username
        self.password = password
        self.client = None
    
    
    def connect(self):
        """Establish an SSH connection to the server."""
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            hostname=self.hostname,
            port=self.port,
            username=self.username,
            password=self.password
        )


    def execute_command(self, command):
        """Execute a command on the remote server."""
        if self.client is None:
            raise Exception("Connection not established. Call connect() first.")
        
        stdin, stdout, stderr = self.client.exec_command(command)
        return stdout.read().decode(), stderr.read().decode()


    def close(self):
        """Close the SSH connection"""
        if self.client:
            self.client.close()
            self.client = None
            print(f'Disconnected from {self.hostname}')
