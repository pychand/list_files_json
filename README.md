Description
pyls is a Python script that mimics the behavior of the ls command in Linux. It takes a JSON file containing directory information as input and prints out its content in the console in the style of ls.


Command Line Arguments
ls: Lists the top-level directories and files.
-A: Lists all files and directories, including those starting with a dot.
-l: Prints results vertically with additional information.
-r: Prints the results in reverse order.
-t: Prints the results sorted by time_modified (oldest first).
--filter=<option>: Filters the output based on the given option (valid options: file, dir).
-h: Shows human-readable sizes.
--help: Shows a helpful message.

Handling Paths
The program can navigate the structure within the JSON.
If the path is a file, it lists the file itself.
It handles relative paths within the directory.

Bonus
Includes a pyproject.toml file to configure installation with pip.
Adds the pyls system command to the system.
