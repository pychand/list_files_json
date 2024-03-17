# tests/test_main.py
import os
import pytest
import sys

script_dir = os.path.dirname(os.path.realpath(__file__))
print(script_dir)
sys.path.append(script_dir)
from pyls.__main__ import ls, format_size

@pytest.fixture
def directory_structure():
    return {
    "name": "interpreter",
    "size": 4096,
    "time_modified": 1699957865,
    "permissions": "-rw-r--r--",
    "contents": [
        {
            "name": ".gitignore",
            "size": 8911,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
        },
        {
            "name": "LICENSE",
            "size": 1071,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
        },
        {
            "name": "README.md",
            "size": 83,
            "time_modified": 1699941437,
            "permissions": "drwxr-xr-x"
        },
        {
            "name": "ast",
            "size": 4096,
            "time_modified": 1699957739,
            "permissions": "-rw-r--r--",
            "contents": [
                {
                    "name": "go.mod",
                    "size": 225,
                    "time_modified": 1699957780,
                    "permissions": "-rw-r--r--"
                },
                {
                    "name": "ast.go",
                    "size": 837,
                    "time_modified": 1699957719,
                    "permissions": "drwxr-xr-x"
                }
            ]
        }     
        ]
    }

def test_ls_with_no_arguments(directory_structure, capsys):
    # Test ls function with no arguments
    ls(directory_structure)
    captured = capsys.readouterr()
    assert captured.out.strip() == "LICENSE\nREADME.md\nast"

def test_ls_with_show_all_option_enabled(directory_structure, capsys):
    # Test ls function with the -A option enabled
    ls(directory_structure, show_all=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == ".gitignore\nLICENSE\nREADME.md\nast"

def test_ls_with_long_format_option_enabled(directory_structure, capsys):
    # Test ls function with the -l option enabled
    ls(directory_structure, long_format=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "-rwxr-xr-x 1071 Nov 14 11:27 LICENSE\n" \
                                    "-rwxr-xr-x 83 Nov 14 11:27 README.md\n" \
                                    "drw-r--r-- 4096 Nov 14 15:58 ast"

def test_ls_with_reverse_option_enabled(directory_structure, capsys):
    # Test ls function with the -r option enabled
    ls(directory_structure, reverse=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "ast\nREADME.md\nLICENSE"

def test_ls_with_sort_by_time_option_enabled(directory_structure, capsys):
    # Test ls function with the -t option enabled
    ls(directory_structure, sort_by_time=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "LICENSE\nREADME.md\nast"

def test_ls_with_filter_option_file_enabled(directory_structure, capsys):
    # Test ls function with the --filter=file option enabled
    ls(directory_structure, filter_option='file')
    captured = capsys.readouterr()
    assert captured.out.strip() == "LICENSE\nREADME.md"

def test_ls_with_filter_option_dir_enabled(directory_structure, capsys):
    # Test ls function with the --filter=dir option enabled
    ls(directory_structure, filter_option='dir')
    captured = capsys.readouterr()
    assert captured.out.strip() == "ast"

def test_ls_with_specific_path(directory_structure, capsys):
    # Test ls function with a specific path provided
    ls(directory_structure, path='ast')
    captured = capsys.readouterr()
    assert captured.out.strip() == "go.mod\nast.go"

def test_ls_with_non_existent_path(directory_structure, capsys):
    # Test ls function with a non-existent path provided
    ls(directory_structure, path='non_existent_path')
    captured = capsys.readouterr()
    assert captured.out.strip() == "error: cannot access 'non_existent_path': No such file or directory"

def test_ls_with_human_readable_size_formatting(directory_structure, capsys):
    # Test ls function with human-readable size formatting enabled
    ls(directory_structure,long_format=True, human_readable=True)
    captured = capsys.readouterr()
    assert captured.out.strip() == "-rwxr-xr-x 1.0 KB Nov 14 11:27 LICENSE\n" \
                                    "-rwxr-xr-x 83 B Nov 14 11:27 README.md\n" \
                                    "drw-r--r-- 4.0 KB Nov 14 15:58 ast"
    
def test_format_size():
    assert format_size(1023) == "1023 B"
    assert format_size(1024) == "1.0 KB"
    assert format_size(1024 * 1024) == "1.0 MB"
    assert format_size(1024 * 1024 * 1024) == "1.0 GB"
    assert format_size(1024 * 1024 * 1024 * 1024) == "1.0 TB"
