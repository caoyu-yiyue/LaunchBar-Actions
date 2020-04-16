#!/usr/bin/env python3

from pathlib import Path
import sys

for input_folder in sys.argv[1:]:
    current_path = Path(input_folder).absolute()
    parent_path = current_path.parent
    all_files = current_path.glob('*')

    for single_f in all_files:
        single_f.rename(parent_path / single_f.name)

    current_path.rmdir()
