import sys
import random
from pyfiglet import Figlet, FigletFont
 
f = Figlet()
fonts = FigletFont.getFonts()
 
if len(sys.argv) == 1:
    font = random.choice(fonts)
elif len(sys.argv) == 3:
    if sys.argv[1] not in ("-f", "--font"):
        sys.exit("Invalid flag. Use -f or --font.")
    if sys.argv[2] not in fonts:
        sys.exit(f"Invalid font: '{sys.argv[2]}'")
    font = sys.argv[2]
else:
    sys.exit("Usage: python figlet.py [-f | --font <font>]")
 
f.setFont(font=font)
text = input("Input: ")
print(f.renderText(text))
