from PIL import Image, ImageMath

stegged=Image.open("stegano.png")
red, green, blue = stegged.split()
secret=ImageMath.eval("(a&0x1)*255",a=red) # convert to 0 or 255
secret=secret.convert("L")
secret.show()
secret.save("secret-retrouve.png")
