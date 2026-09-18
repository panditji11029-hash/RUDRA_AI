import system_tools
import file_tools
from tools import calculate


class ToolManager:

    def __init__(self):
        self.tools = {
            "system_info": self.system_info,
            "current_time": self.current_time,
            "current_date": self.current_date,
            "list_files": self.list_files,
            "calculate": self.calculate,
            "create_folder": self.create_folder,
            "read_file": self.read_file,
            "create_file": self.create_file,
            "check_file": self.check_file
        }

    # -----------------------------------------------------
    # SYSTEM
    # -----------------------------------------------------

    def system_info(self):

        info = system_tools.system_info()

        lines = [
            "RUDRA SYSTEM INFORMATION",
            "────────────────────────────────"
        ]

        for key, value in info.items():
            lines.append(
                f"{key}: {value}"
            )

        return "\n".join(lines)

    def current_time(self):

        return (
            f"Current time is "
            f"{system_tools.current_time()}."
        )

    def current_date(self):

        return (
            f"Today's date is "
            f"{system_tools.current_date()}."
        )

    def list_files(self):

        return (
            "RUDRA FILE SYSTEM\n"
            "────────────────────────────────\n"
            + system_tools.list_folder(".")
        )

    # -----------------------------------------------------
    # CALCULATOR
    # -----------------------------------------------------

    def calculate(self, expression):

        result = calculate(
            expression
        )

        if result is None:
            return "Invalid mathematical expression."

        return str(result)

    # -----------------------------------------------------
    # FILES
    # -----------------------------------------------------

    def create_folder(self, name):

        if not name:
            return "Please provide a folder name."

        return file_tools.create_folder(
            name
        )

    def read_file(self, name):

        if not name:
            return "Please provide a file name."

        return file_tools.read_file(
            name
        )

    def create_file(
        self,
        name,
        content=""
    ):

        if not name:
            return "Please provide a file name."

        return file_tools.create_text_file(
            name,
            content
        )

    def check_file(self, name):

        if not name:
            return "Please provide a file name."

        if file_tools.file_exists(
            name
        ):

            return (
                f"Yes, '{name}' exists."
            )

        return (
            f"No, '{name}' was not found."
        )

    # -----------------------------------------------------
    # TOOL EXECUTION
    # -----------------------------------------------------

    def execute(
        self,
        tool_name,
        *args
    ):

        tool = self.tools.get(
            tool_name
        )

        if not tool:

            return (
                f"Unknown tool: "
                f"{tool_name}"
            )

        try:

            return tool(
                *args
            )

        except Exception as error:

            return (
                f"Tool execution error: "
                f"{error}"
            )

    # -----------------------------------------------------
    # TOOL LIST
    # -----------------------------------------------------

    def available_tools(self):

        return list(
            self.tools.keys()
        )


tool_manager = ToolManager()