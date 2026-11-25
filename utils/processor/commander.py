import os
import platform
import subprocess
import webbrowser

import pandas as pd
from tabulate import tabulate

from utils.exception.operating_system_implementation_required_exception import OperatingSystemImplementationRequiredAppException
from utils.processor.print_processor import color_text, GREEN_TEXT


def empty_string(data):
    return data is None or data.strip() == ""


class Commander:
    @staticmethod
    def get_terminal_name():
        return OSCommander.run(
            linux=lambda: "gnome-terminal",
        )

    @staticmethod
    def execute(commands, show=False, sync=False):
        if sync:
            subprocess.run(commands, shell=True)

        else:
            process = subprocess.run(commands, capture_output=True, shell=True)
            output = process.stdout.decode("utf-8")
            if show:
                print(output)
            return output

    @staticmethod
    def execute_externally(command_to_run, python=False):
        """This is deprecated"""
        Commander.execute_shell(command_to_run)
        # subprocess.run(["python", "exec.py"])
        # if python:
        #     command_to_run = f"python exec.py -k {command_to_run}"
        # else:
        # execute_script_file_path = os.path.join(os.path.abspath(os.getcwd()), "exec.sh")

        # subprocess.Popen([execute_script_file_path, command_to_run], shell=True)

        ### Frozen input
        # output = subprocess.run(
        #     [execute_script_file_path, command_to_run],
        #     shell=True,
        #     stdout=subprocess.PIPE,
        #     text=True,
        # )
        # print("Executing Command {}".format(command_to_run))
        # subprocess.Popen(['gnome-terminal', '-e', 'bash', '-c', 'exec.sh', 'echo "Hello from shell script"'])

        # output = subprocess.Popen(['gnome-terminal', '-e', 'bash', 'exec.sh', command_to_run], shell=True,
        #                           stdout=subprocess.PIPE, text=True)
        # print("Finished")
        # print(output.stdout)

    @staticmethod
    def execute_shell(command, external=True):
        if not external:
            Commander.execute(command)
        else:
            exec_file = os.path.join(os.getcwd(), "exec.sh")
            OSCommander.run(
                linux=lambda: subprocess.Popen(
                    ["gnome-terminal", "--", exec_file, command],
                    cwd=os.getcwd(),
                ),
                windows=lambda: subprocess.Popen(
                    ["cmd.exe", "/c", "start", exec_file, command],
                    cwd=os.getcwd()
                )
            )

    @staticmethod
    def execute_python(execute=None, args=None, sync=False):
        print(os.getcwd())
        if args is None:
            args = []
            if sync:
                args.append("sync")
        OSCommander.run(
            windows=lambda: (
                subprocess.Popen(
                    ["start", "cmd", "/k", "python", "pilot.py", "" if execute is None else f"exec='{execute}'"] + args,
                    shell=True,
                )
            ),
            linux=lambda: (
                subprocess.Popen(
                    ["gnome-terminal", "--", "python3", "pilot.py", f"exec='{execute}'"] + args,
                    cwd=os.getcwd(),
                )
            )
        )

    @staticmethod
    def open_url(url: str):
        webbrowser.open(url, new=0, autoraise=True)

    @staticmethod
    def print(commands):
        print(Commander.execute(commands))

    @staticmethod
    def print_table(data):
        df = pd.DataFrame(data)
        table = tabulate(df, headers="keys", tablefmt="pretty")
        print(table)

    @staticmethod
    def persistent_input(query, optional_data=None):
        query += (
                     " (default: " + (color_text(GREEN_TEXT, optional_data) + ")")
                     if optional_data is not None
                     else ""
                 ) + ": "
        while True:
            data = input(query)
            # query + ("(" + color_text(GREEN_TEXT, optional_data) + ")") if optional_data is not None else "" + ": ")
            if empty_string(data):
                if optional_data is not None:
                    return optional_data
                else:
                    continue
            return data

    @staticmethod
    def synthesize_path(path: str):
        return path.replace("\\", "/")

    @staticmethod
    def path_exist(path: str):
        path = Commander.synthesize_path(path)
        return os.path.exists(path)

    @staticmethod
    def open_with_notepad(file_path):
        Commander.execute(CommandStringGenerator.launch_notepad(file_path))

    @staticmethod
    def on_key_press():
        pass



class OSCommander:
    os = platform.system()

    @staticmethod
    def run(windows=None, linux=None, mac=None, common=None):
        if common is not None:
            return common()
        elif OSCommander.os == "Windows":
            if windows is None:
                raise OperatingSystemImplementationRequiredAppException(OSCommander.os)
            return windows()
        elif OSCommander.os == "Linux":
            if linux is None:
                raise OperatingSystemImplementationRequiredAppException(OSCommander.os)
            return linux()
        elif OSCommander.os == "Mac":
            if linux is None:
                raise OperatingSystemImplementationRequiredAppException(OSCommander.os)
            return mac()
        else:
            raise OperatingSystemImplementationRequiredAppException(OSCommander.os)

class CommandStringGenerator:
    @staticmethod
    def launch_notepad(file_path):
        # Try to use FileReaderProcessor.open_file_with_notepad
        return OSCommander.run(
            linux=lambda: f"xdg-open {file_path}",
            windows=lambda: f"notepad.exe {file_path}",
            mac=lambda: f"gedit {file_path}"
        )

    @staticmethod
    def ping(domain):
        return OSCommander.run(
            linux=lambda: f"ping -c 5 {domain}",
            windows=lambda: f"ping -n 5 {domain}"
        )

    @staticmethod
    def remove_subdirectories(path):
        return OSCommander.run(
            linux=lambda: f"rm -rf {os.path.join(path, '*')}"
        )

    @staticmethod
    def kubernetes_scale(namespace, deployment_name, down=False, stateful_set=False):
        return OSCommander.run(
            common=lambda: f"kubectl scale -n {namespace} {'statefulset' if stateful_set else 'deployment'} {deployment_name} --replicas={'0' if down else '1'};"
        )

    @staticmethod
    def kubernetes_apply_deployment_config(file_path, namespace):
        return OSCommander.run(
            common=lambda: f"kubectl apply deployment -f {file_path} -n {namespace}"
        )
