from PIL import Image, ImageFilter, ImageMath

# Load an image from the hard drive
original = Image.open("original.jpg")
secret = Image.open("secret.jpg").resize(original.size)
# Convert to black and white
secret = secret.convert('1')
# Split channels
r, g, b = original.split()
# Encode the secret in the last bit of the red channel
out = ImageMath.eval("convert(a&254|b&1,'L')", a=r, b=secret)
stegano = Image.merge("RGB", (out, g, b))

stegano.show()
stegano.save("stegano.png")


