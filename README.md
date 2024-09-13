# Spritesheeter
Generate spritesheets of multiple png from source folder contents

![preview](preview.png?raw=true "create spritesheet")

# Installation
```
pip install pillow prompt_toolkit
``` 

# Use
```
python .\main.py -n Frank -a "Idle, Walk" -p "./src"
```
## Sprites
Sprite filename format ```NAME_ACTION_DIRECTION__NR.png```  

e.g.  
Frank_Idle_F__0000.png,  
Frank_Idle_F__0001.png,  
Frank_Idle_F__0002.png,  
Frank_Idle_B__0000.png,  
...
