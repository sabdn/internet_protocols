class ServerAnswer:
    def __init__(self, msg: str):
        self._parse_msg(msg)

    def _parse_msg(self, msg: str):
        self.all_msg = msg
        msg_parts = msg.split('\n')[:-1]
        self.last_code = int(msg_parts[-1][0:4])
        self.last_msg = msg_parts[-1][5:]

    def __str__(self):
        return self.all_msg
