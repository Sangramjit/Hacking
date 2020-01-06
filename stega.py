from PIL import Image, ImageFont, ImageDraw
import textwrap

def decode_image(file_location="images_sample.png"):

    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    size1 = encoded_image.size[0]
    size2= encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for i in range(size1):
        for j in range(size2):
            if bin(red_channel.getpixel((i, j)))[-1] == '0':
                pixels[i, j] = (255, 255, 255)
            else:
                pixels[i, j] = (0,0,0)
    decoded_image.save("images/decode.png")

def write_text(text_to_write, image_size):
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin,offset), line, font=font)
        offset += 10
    return image_text

def encode_image(text_to_encode, template_image="images/xyz.jpg"):
    template_image = Image.open(template_image)
    red_template = template_image.split()[0]
    green_template = template_image.split()[1]
    blue_template = template_image.split()[2]

    size1 = template_image.size[0]
    size2 = template_image.size[1]

    image_text = write_text(text_to_encode, template_image.size)
    bw_encode = image_text.convert('1')

    encoded_image = Image.new("RGB", (size1, size2))
    pixels = encoded_image.load()
    for i in range(size1):
        for j in range(size2):
            red_template_pix = bin(red_template.getpixel((i,j)))
            old_pix = red_template.getpixel((i,j))
            ddecode_pix = bin(bw_encode.getpixel((i,j)))

            if ddecode_pix[-1] == '1':
                red_template_pix = red_template_pix[:-1] + '1'
            else:
                red_template_pix = red_template_pix[:-1] + '0'
            pixels[i, j] = (int(red_template_pix, 2), green_template.getpixel((i,j)), blue_template.getpixel((i,j)))

    encoded_image.save("images/encoded_image.png")

if __name__ == '__main__':
    decode_image()
    encode_image("Hey Viewers!!")

