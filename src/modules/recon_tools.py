class ReconTools:
    def __init__(self):
        self.function_map = {
            "subdomain": [
                self.subdomain,
                self.brutedns,
                self.permutation,
                self.dnsprobe,
                self.tls,
            ],
            "port": [self.port_scan],
            "http": [self.httprobe],
            "aquatone": [self.aquatone],
            "spider": [self.spider],
            "gf": [self.gf],
            "nuclei": [self.nuclei],
            "xss": [self.xss],
            "fuzzing": [self.fuzzing],
            # "password": [leak_password]
        }

    def subenum(self):
        return

    def dnsprobe(self):
        return
