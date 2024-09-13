import os
import argparse
import glob
from pathlib import Path
from PIL import Image
from prompt_toolkit import prompt

class Sprite:
	def __init__(self, path):
		self.path = Path(path)
		self.size = Image.open(self.path).size
	def __str__(self):
		return f'Sprite<size: {self.size}, path: {self.path}>'
	def get_image(self):
		return Image.open(self.path)
	def get_action(self):
		return Path(self.path).stem.split('_')[1]
	def get_direction(self):
		return Path(self.path).stem.split('_')[2]
	def get_nr(self):
		return Path(self.path).stem.split('_')[4]

class Spritesheet:
	# __init__()
	# Constructor
	#
	# @returns: void
	def __init__(self, name, path = './', output = './', action = None):
		self.name = name
		self.path = path
		self.output = output
		self.actions = action.split(', ') if action is not None else [None]
		self.sprites = []

		for a in self.actions:
			for sprite_path in glob.glob(f'{path}/{name}_{a if a is not None else ""}*.png'):
				self.sprites.append(Sprite(sprite_path))	

		self.actions = self.get_actions(self.sprites)

	# __str__()
	# returns readable string
	#
	# @returns: fstring
	def __str__(self):
		return f'Spritesheet<name: {self.name}, length: {len(self.sprites)}>'

	# sprite_size_max()
	# returns largest size in pixel from given spritelist
	#
	# @returns: tuple<int, int>
	def get_size_max(self, spr_list):
		w = 0
		h = 0
		for spr in spr_list:
			h = int(spr.size[1]) if int(spr.size[1]) > h else h
			w = int(spr.size[0]) if int(spr.size[0]) > w else w
		return (w,h)

	# get_coords_max()
	# returns coords max from given spritelist
	#
	# @returns: tuple<int, int>
	def get_coords_max(self, spr_list):
		rows = 0
		cols = []
		for sprite in spr_list:
			rows = int(sprite.get_nr()) if int(sprite.get_nr()) > rows else rows
			if sprite.get_direction() not in cols:
				cols.append(sprite.get_direction())
		return (rows + 1, len(cols))

	# get_actions()
	# returns list of actions from given spritelist
	#
	# @returns: list<str>
	def get_actions(self, spr_list):
		actions = []
		for sprite in spr_list:
			if sprite.get_action() not in actions:
				actions.append(sprite.get_action())
			
		return actions

	# get_filtered()
	# get list filtered by action from given spritelist
	#
	# @returns: list<Sprite>
	def get_filtered_sprites(self, action, spr_list):
		sprites = []
		for spr in spr_list:
			if str(spr.get_action()) == str(action):
				sprites.append(spr)
		return sprites

	# generate()
	#
	# @returns: list<Image>
	def generate(self, verbose = True):
		if (verbose):
			print(f'\n# GENERATE SPRITESHEET ################################################')
		
		sheets = []
		for action in self.actions:
			if (verbose):
				print(f'\n  Spritesheet for [{action}]:')
			
			filtered_list = self.get_filtered_sprites(action, self.sprites)

			w,h = self.get_size_max(filtered_list)
			r,c = self.get_coords_max(filtered_list)

			if (verbose):
				print(f'  ---------------------------------------------------------------------\n')
				print(f'  > {len(filtered_list)} sprites')
				print(f'  > {r} x {c} layout')
				print(f'  > {w*r} x {h*c}px')

			try:
				ss = Image.new('RGBA', (w*r, h*c))
				for idx, spr in enumerate(filtered_list):
					x = int(idx % int(r)) * int(w)
					y = int(idx / int(r)) * int(h)
				
					ss.paste(spr.get_image(), (x, y))
				ss.save(Path(f'{self.output}/SSheet_{self.name}_{action}.png'))
				sheets.append(ss)
				if (verbose):
					print(f'\n  successfully generated.')
			except:
				print(f'failed spritesheet [{action}]')

			if (verbose):
				print(f'  ---------------------------------------------------------------------\n')

		if (verbose):
			print(f'\n  done.\n')

		return sheets


# console cleanup
# CLEAR_CONSOLE = lambda: os.system('cls')
# CLEAR_CONSOLE()

# argument parser
PARSER = argparse.ArgumentParser(
	prog='SpritesheetGenerator',
	description='Generates a spritesheet from directory of sprites. Filename format needs to be "name_action_direction__0000.png"'
)

PARSER.add_argument('-n', '--name', help='sprite name')
PARSER.add_argument('-a', '--action', help='actions split by a comma e.g. -a "Idle, Walk"')
PARSER.add_argument('-p', '--path', help='source folder defaults to ./')
PARSER.add_argument('-o', '--output', help='export folder defaults to path')

ARGS = PARSER.parse_args()

# user input
inName   = ARGS.name   if ARGS.name   is not None else prompt('Spritename to look for :> ')
inPath   = ARGS.path   if ARGS.path   is not None else './'
inOutput = ARGS.output if ARGS.output is not None else inPath
inAction = ARGS.action

sheet = Spritesheet(inName, inPath, inOutput, inAction)
sheet.generate(True)
