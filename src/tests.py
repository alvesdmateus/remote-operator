import os

playbook_dir = "/etc/ansible/playbooks/"
playbook_name = "sample_playbook"

print(os.path.join(playbook_dir, playbook_name))