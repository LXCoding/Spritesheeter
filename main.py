import os
import argparse

from gen import Generator

# argument parser
PARSER = argparse.ArgumentParser(
	prog='SpritesheetGenerator',
	description='Generates a spritesheet from directory of sprites. Filename format needs to be "name_action_direction__0000.png"'
)

PARSER.add_argument('-a', '--action'	, help='actions split by a comma e.g. -a "Idle, Walk"')
PARSER.add_argument('-p', '--path'		, help='source folder defaults to ./')
PARSER.add_argument('-m', '--mirror'	, help='generate mirrored sprites')
PARSER.add_argument('-o', '--output'	, help='export folder defaults to path')

ARGS = PARSER.parse_args()

# user input
inPath   = ARGS.path   if ARGS.path   is not None else './src'
inOutput = ARGS.output if ARGS.output is not None else './export'
inMirror = ARGS.mirror if ARGS.mirror is not None else False
inAction = ARGS.action

sheet = Generator(
	path = inPath, 
	action = inAction, 
	mirror_faces = inMirror, 
	output = inOutput
)
sheet.make()
