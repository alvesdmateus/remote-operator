import ansible_manager, ssh_connection, ssh_connection


class RemoteOperator:
    def __init__(self, ansible_object, input_object):
        self.ansible_object = ansible_object
        self.input_object = input_object

    def setup_ansible(self):
        self.ansible_object.setup_ansible()

    def register_hosts_in_inventory(self, hosts_filename, group="all"):
        self.input_object.set_hosts_input(hosts_filename)
        server_list = self.input_object.get_server_list()
        self.ansible_object.register_hosts(server_list, group)

    def register_private_key(self, private_key):
        self.ansible_object.register_private_key(private_key)

    def create_playbook(self, playbook_name, content):
        if os.path.isfile(content):
            with open(content, "r") as file:
                content = file.read()

        self.ansible_object.create_playbook(playbook_name, content)

    def run_playbook(self, playbook_name, group="all"):
        self.ansible_object.run_playbook(
            playbook_name,
            group,
        )

    def get_input(self):
        return self.input_object.slice_domains()
