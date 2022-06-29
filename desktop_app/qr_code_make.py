import qrcode


def create_qr(url):
    qr = qrcode.QRCode(version=2, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=4, border=1)
    qr.add_data(url)
    qr.make(fit=True)
    image = qr.make_image()
    image.save("static/img/client.png")


if __name__ == "__main__":
    create_qr(url='Hello Lab')