#!/usr/bin/env python3
"""Directed corner replay; all output is inside o2cert."""
import pathlib, sys, os
ROOT=pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src/corner_impl'))
os.chdir(ROOT)
from run_corner import main
raise SystemExit(0 if main()==0 else 1)
