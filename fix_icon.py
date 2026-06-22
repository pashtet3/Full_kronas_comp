from PIL import Image

img = Image.open("icon.ico")  # або твій PNG якщо є

img.save(
    "icon_fixed.ico",
    sizes=[(16,16), (32,32), (48,48), (64,64), (128,128), (256,256)]
)