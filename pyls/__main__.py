# main.py
import argparse
import datetime
import json
import os
import stat
from typing import Dict
import time

def load_directory_structure(file_path: str) -> Dict:
    with open(file_path, 'r') as file:
        return json.load(file)

def get_permissions(item: Dict) -> str:
    """
    Convert file mode to human-readable permission string.

    Args:
        mode (str): File mode.

    Returns:
        str: Human-readable permission string.
    """
    permissions = item['permissions']
    mode = ''

    if(item.get('contents')):
        mode = 'd' + permissions[1:]
    else:
        mode = '-' + permissions[1:]
    return mode


def format_size(size: int) -> str:
    suffixes = ['B', 'KB', 'MB', 'GB', 'TB']
    index = 0
    while size >= 1024 and index < len(suffixes) - 1:
        size /= 1024.0
        index += 1
        
    if suffixes[index] == 'B':
        return f"{size} {suffixes[index]}"
    else:
        return f"{size:.1f} {suffixes[index]}"

def ls(directory_structure: Dict, path: str = '', show_all: bool = False, long_format: bool = False, reverse: bool = False, sort_by_time: bool = False, filter_option: str = None, human_readable: bool = False) -> None:
    modified_path = False
    if path:
        current_directory = directory_structure
        for directory in path.split('/'):
            found = False
            for item in current_directory.get('contents', []):
                if item['name'] == directory:
                    current_directory = item
                    found = True
                    break
            if 'contents' not in current_directory:
                current_directory['name'] = "./" + path
                modified_path = True

            if not found:
                print(f"error: cannot access '{path}': No such file or directory")
                return
    else:
        current_directory = directory_structure


    if "contents" in current_directory:
        contents = current_directory['contents']
    else:
        contents=[current_directory,]
    
        
    if filter_option:
        if filter_option == 'file':
            contents = [item for item in contents if not item.get('contents')]
        elif filter_option == 'dir':
            contents = [item for item in contents if  item.get('contents')]

    if sort_by_time:
        contents.sort(key=lambda x: x['time_modified'])
    if reverse:
        contents = reversed(contents)
    for item in contents:
        if show_all or not item['name'].startswith('.') or modified_path:
            if long_format:
                mode = get_permissions(item)
                size = item['size']
                mtime = datetime.datetime.fromtimestamp(item['time_modified']).strftime('%b %d %H:%M')
                if human_readable:
                    size = format_size(size)
                print(f"{mode} {size} {mtime} {item['name']}")
            else:
                print(item['name'])

def custom_help_message():
    print("Custom help message:")
    print("-A:      List all files and directories, including hidden ones")
    print("-l:      Use a long listing format")
    print("-r:      Reverse order")
    print("-t:      Sort by modification time, newest first")
    print("--filter {file, dir}: Filter the output based on the given option (file or dir)")
    print("--help:  Show this help message and exit")

def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument('-A', action='store_true', help='List all files and directories, including hidden ones')
    parser.add_argument('-l', action='store_true', help='Use a long listing format')
    parser.add_argument('-r', action='store_true', help='Reverse order')
    parser.add_argument('-t', action='store_true', help='Sort by modification time, newest first')
    parser.add_argument('--filter', dest='filter_option', choices=['file', 'dir'], help='Filter the output based on the given option (file or dir)')
    parser.add_argument('-h', action='store_true', help='Show human-readable sizes')
    parser.add_argument('path', nargs='?', default='', help='Path to directory to list')
    parser.add_argument('--help', action='store_true', help='Show this help message and exit')
    args = parser.parse_args()

    script_dir = os.path.dirname(os.path.realpath(__file__))
    directory_structure = load_directory_structure(os.path.join(script_dir,'example_structure.json'))
    if args.help:
        custom_help_message()
        exit()
    ls(directory_structure, path=args.path, show_all=args.A, long_format=args.l, reverse=args.r, sort_by_time=args.t, filter_option=args.filter_option, human_readable=args.h)

if __name__ == "__main__":
    main()
