# Spritesheeter
spritesheet generator using pillow  
creates flipped version from right to left

![preview](preview.png?raw=true "create spritesheet")

```
python .\main.py
python .\main.py -a "Idle, Walk" -p "./src" -m True -o "./export"
```
Sprite filename format ```NAME_ACTION_DIRECTION__NR.png```  
e.g.  
Frank_Idle_F__0000.png,  
Frank_Idle_F__0001.png,  
Frank_Idle_F__0002.png,  
Frank_Idle_B__0000.png,  
...
