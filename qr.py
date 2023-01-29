import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import SquareGradiantColorMask
import sys, getopt
from os import path
from PIL import Image, ImageDraw
from math import sqrt

BASE_WIDTH = 100
HIGH_CORRECTION = qrcode.constants.ERROR_CORRECT_H


def add_resized_logo(qr_img, logo_path):
    print("- Adding logo:", logo_path)
    try:
        logo_img = Image.open(logo_path)
        wpercent = BASE_WIDTH / float(logo_img.size[0])
        hsize = int((float(logo_img.size[1]) * float(wpercent)))
        logo_img = logo_img.resize((BASE_WIDTH, hsize), Image.Resampling.LANCZOS)

        top_left_logo_position = (
            (qr_img.size[0] - logo_img.size[0]) // 2,
            (qr_img.size[1] - logo_img.size[1]) // 2,
        )

        qr_img.paste(logo_img, top_left_logo_position, logo_img)
    except FileNotFoundError:
        print("- Logo not found, step ignored")

    return qr_img


def get_qr_img(text, logo_file):
    qr = qrcode.QRCode(error_correction=HIGH_CORRECTION)
    qr.add_data(text)

    blue = (0, 0, 255)
    red = (255, 0, 0)

    qr_img = qr.make_image(
        image_factory=StyledPilImage,
        eye_drawer=RoundedModuleDrawer(radius_ratio=1.5),
        module_drawer=RoundedModuleDrawer(),
        color_mask=SquareGradiantColorMask(center_color=blue, edge_color=red),
    )

    if logo_file != None:
        qr_img = add_resized_logo(qr_img, path.join("logos", logo_file))

    return qr_img


def is_allowed(char):
    return char.isalnum() or char in ("-", "_", ".")


def clean_filename(file_name):
    file_name_allowed_chars = "".join(c for c in file_name if is_allowed(c))
    return file_name_allowed_chars.replace("..", "")


def main(argv):
    input_text = None
    output_file = "qr"
    logo_file = None
    opts, args = getopt.getopt(argv, "ht:o:l:", ["text=", "output=", "logo="])
    for opt, arg in opts:
        if opt == "-h":
            print("qr.py -t <input_text> -o <output_file>")
            sys.exit()
        elif opt in ("-t", "--text"):
            input_text = arg.strip()
        elif opt in ("-o", "--output"):
            output_file = clean_filename(arg.strip())
        elif opt in ("-l", "--logo"):
            logo_file = clean_filename(arg.strip())

    if len(output_file) == 0:
        print("Filename cannot be empty")
    elif len(input_text) > 0:
        print("Generating QR Code for:", input_text)
        img = get_qr_img(input_text, logo_file)

        print("- Saving QR Code at: output/{}".format(output_file))
        img.save(path.join(".", "output", "{}".format(output_file)))

        print("DONE")
    else:
        print("You need to define an input text")


if __name__ == "__main__":
    main(sys.argv[1:])
