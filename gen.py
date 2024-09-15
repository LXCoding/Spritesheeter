import glob

from pathlib import Path
from PIL import Image, ImageOps

class Sprite:
	def __init__(self, path):
		self.path = Path(path)
		self.size = Image.open(self.path).size
	def __str__(self):
		return f'Sprite<size: {self.size}, path: {self.path} face: {self.face()}>'
	def img(self):
		return Image.open(self.path)
	def action(self):
		return Path(self.path).stem.split('_')[1]
	def face(self):
		return Path(self.path).stem.split('_')[2]
	def nr(self):
		return Path(self.path).stem.split('_')[4]

class Generator:
	def __init__(self, path = './', action = None, mirror_faces = False, img_format = 'png', output = './export'):
		self.name = ''
		self.path = path
		self.output = output
		self.format = img_format
		self.sprites = []
		self.scan(action)
		
		if mirror_faces:
			self.mirror()

	def __str__(self):
		return f'Generator<elements: {len(self.sprites)}, path: {self.path}, size: {self.size("idle")}>'

	def x(self, action):
		count = -1
		for s in self.sprites:
			if s.action() == action and int(s.nr()) > int(count):
				count += 1
		return count + 1 if count != -1 else -1

	def y(self, action):
		faces = []
		for s in self.sprites:
			if s.action() == action and s.face() not in faces:
				faces.append(s.face())
		return len(faces)

	def size(self, action):
		w = 0
		h = 0
		
		for spr in self.sprites:
			if spr.action() == action:
				w = int(spr.size[0]) if int(spr.size[0]) > w else w
				h = int(spr.size[1]) if int(spr.size[1]) > h else h

		return (w * self.x(action), h * self.y(action))

	def actions(self):
		actions = []
		for spr in self.sprites:
			if spr.action() not in actions:
				actions.append(spr.action())
		return actions
	
	def faces(self, action):
		faces = []
		for spr in self.sprites:
			if spr.face() not in faces and spr.action() == action:
				faces.append(spr.face())
		return faces

	def mirror(self):
		for action in self.actions():
			for p in glob.glob(f'{self.path}/*_{action}_R*__*.{self.format}'):
				ps = p.split('_')
				spr = Image.open(p)
				
				newFilename = Path(f'{ps[0]}_{ps[1]}_{ps[2].replace("R", "L")}__{ps[4]}')
				newImage = Image.new('RGBA', spr.size)
				newImage.paste(spr, (0,0))
				newImage = newImage.transpose(Image.FLIP_LEFT_RIGHT)
				newImage.save(newFilename)

				self.sprites.append(Sprite(newFilename))
		return

	def filtered(self, action):
		f = []
		for s in self.sprites:
			if s.action() == action:
				f.append(s)
		return f

	def scan(self, action):
		spr_action = action.split(', ') if action != None else [None]
		self.sprites.clear()
		for a in spr_action:
			for spr_path in glob.glob(f'{self.path}/*_{a if a is not None else ""}*__*.{self.format}'):
				self.sprites.append(Sprite(spr_path))

	def make(self):
		sheets = []
		for action in self.actions():
			print(f'Generate {action}: {self.size(action)}')
			canvas = Image.new('RGBA', self.size(action))
			
			for idx, sprite in enumerate(self.filtered(action)):
				posx = int(idx % self.x(action))
				posy = int(idx / self.x(action))
				canvas.paste(sprite.img(), (posx * sprite.size[0], posy * sprite.size[1]))
			canvas.save(f'{self.output}/SSheet_{action}.{self.format}')
			sheets.append(canvas)
		return sheets
