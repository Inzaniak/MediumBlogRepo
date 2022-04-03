import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles.colormasks import ImageColorMask
from PIL import Image

logo = Image.open('logo/newlogo.png')

qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_L
    , version = 2
    , border=1
    , box_size=12,
)
qr.add_data('https://inzaniak.github.io')

qr_img = qr.make_image(image_factory=StyledPilImage, color_mask=ImageColorMask(back_color=(255,255,255), color_mask_image=logo))
qr_img.save('qrcode.png')