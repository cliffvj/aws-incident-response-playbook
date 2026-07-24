#!/usr/bin/env python3
from pathlib import Path
import shutil, zipfile
ROOT=Path(__file__).resolve().parents[1]
BUILD=ROOT/"build"
FUNCTIONS=ROOT/"lambda"
SHARED=ROOT/"shared"/"aws_ir"

def add_tree(zf, source, prefix=""):
    for p in source.rglob("*"):
        if p.is_file() and "__pycache__" not in p.parts:
            zf.write(p, str(Path(prefix)/p.relative_to(source)))

def main():
    if BUILD.exists(): shutil.rmtree(BUILD)
    BUILD.mkdir()
    for function_dir in sorted(p for p in FUNCTIONS.iterdir() if p.is_dir()):
        archive=BUILD/f"{function_dir.name}.zip"
        with zipfile.ZipFile(archive,"w",zipfile.ZIP_DEFLATED) as zf:
            zf.write(function_dir/"app.py","app.py")
            add_tree(zf,SHARED,"aws_ir")
        print(archive)
if __name__=="__main__": main()
