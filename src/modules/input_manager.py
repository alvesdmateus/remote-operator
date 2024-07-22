class InputManager:
    def __init__(self, domains=None, server_list_file=None):
        self.domains = domains
        self.server_list = (
            self.read_server_list(server_list_filename)
            if server_list_file is not None
            else None
        )
        self.num_servers = len(server_list)
        self.servers = {server: [] for server in server_list}

    def read_server_list(self, filename):
        with open(filename, "r") as file:
            servers = [line.strip() for line in file.readlines()]
        return servers

    def set_hosts_input(self, hosts_input):
        if isinstance(hosts_input, list):
            self.server_list = self.read_server_list(hosts_input)
        else:
            self.server_list = hosts_input

    def get_server_list(self):
        return self.server_list

    def slice_domains(self):
        # Calculate the number of domains each server should handle
        num_domains = len(self.domains)
        domains_per_server = num_domains // self.num_servers
        extra_domains = num_domains % self.num_servers

        start_index = 0
        for server in self.server_list:
            end_index = start_index + domains_per_server
            # Distribute the extra domains
            if extra_domains > 0:
                end_index += 1
                extra_domains -= 1
            self.servers[server] = self.domains[start_index:end_index]
            start_index = end_index
        return self.get_servers()

    def get_servers(self):
        return self.servers


if __name__ == "__main__":
    # Example usage
    domains = [
        "domain1.com",
        "domain2.com",
        "domain3.com",
        "domain4.com",
        "domain5.com",
        "domain6.com",
        "domain7.com",
    ]
    server_list = ["server1", "server2", "server3"]

    slicer = DomainSlicer(domains, server_list)
    slicer.slice_domains()
    servers = slicer.get_servers()

    for server, domains in servers.items():
        print(f"{server}: {domains}")
