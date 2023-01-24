import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.moduledrawers import RoundedModuleDrawer
from qrcode.image.styles.colormasks import RadialGradiantColorMask
import sys, getopt
from os import path


def get_qr_img(text):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L)
    qr.add_data(text)

    blue = (0, 0, 255)
    red = (255, 0, 0)

    return qr.make_image(
        image_factory=StyledPilImage,
        color_mask=RadialGradiantColorMask(center_color=blue, edge_color=red),
    )


def is_allowed(char):
    return char.isalnum() or char in ("-", "_")


def clean_filename(file_name):
    return "".join(c for c in file_name if is_allowed(c))


def main(argv):
    input_text = None
    output_file = "qr"
    opts, args = getopt.getopt(argv, "ht:o:", ["text=", "output="])
    for opt, arg in opts:
        if opt == "-h":
            print("qr.py -t <input_text> -o <output_file>")
            sys.exit()
        elif opt in ("-t", "--text"):
            input_text = arg.strip()
        elif opt in ("-o", "--output"):
            output_file = clean_filename(arg.strip())

    if len(output_file) == 0:
        print("Filename cannot be empty")
    elif len(input_text) > 0:
        print("Generating QR Code for:", input_text)
        img = get_qr_img(input_text)
        print("Saving it at: {}.png".format(output_file))
        img.save(path.join(".", "output", "{}.png".format(output_file)))
    else:
        print("You need to define an input text")


if __name__ == "__main__":
    main(sys.argv[1:])
