from rich.console import Console


class CarnivalLogger:
    console = Console()

    def info(self, message: str):
        self.console.print(message, style="bold blue")

    def success(self, message: str):
        self.console.print(message, style="bold green")

    def error(self, message: str):
        self.console.print(message, style="bold red")

    def log(self, message: str):
        self.console.print(message)


logger = CarnivalLogger()
