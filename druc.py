from escpos import printer


if __name__ == "__main__":
    Generic = printer.Usb(0x0456, 0x0808)
