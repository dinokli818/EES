"""Module providing basic ssh server with fabric library."""
from fabric import Connection, Config

class RemoteShell:
    """
    Open a consistent ssh connection with remote server.
    """
    def __init__(self, hostname, port, username, password):
        self.config = Config(overrides={'connect_kwargs': {'password': password}})
        self.connection = Connection(
            host=hostname,
            port=port,
            user=username,
            connect_kwargs={"password": password}
        )
    def execute(self, cmd):
        """
        Using opened ssh connection to execute command in string.

        Args:
            cmd (string): shell command.

        Returns:
            any: result
        """
        result = self.connection.run(cmd, hide=True, shell="/bin/bash -c")
        print(">>>"+cmd+'\n'+result.stdout+'\n')
        return result
    def close(self):
        """
        Close and clear the opened ssh connection.
        """
        self.connection.clear()

if __name__ == "__main__":
    remote_shell = RemoteShell("192.168.225.16", 22, "root", "ftclftcl")
    result = remote_shell.execute("ls")
    if result.exited == 0:
        print("Command executed successfully.")
        print(result.stdout)
    else:
        print("Command execution failed.")
