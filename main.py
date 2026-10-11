import os
from portal import Xbox360Portal
import webserver
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s")

def main():
    portal = Xbox360Portal()
    device = "/dev/hidg0"

    logging.info("Opening HID gadget: %s", device)

    with open(device, "r+b", buffering=0) as hid:
        logging.info("Waiting for reports...")

        while True:
            request = hid.read(32)

            if not request:
                continue

            logging.info("RX (%d): %s", len(request), request.hex(" "))

            response = portal.handle_report(request)

            response = bytes(response)

            logging.info(
                "TX (%d): %s",
                len(response),
                response.hex(" "),
            )

            hid.write(response)

if __name__ == '__main__':
    main()
