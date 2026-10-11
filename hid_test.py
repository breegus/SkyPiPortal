import os
import select

DEVICE = "/dev/hidg0"
REPORT_SIZE = 32

fd = os.open(DEVICE, os.O_RDWR | os.O_NONBLOCK)
print(f"Listening on {DEVICE} ({REPORT_SIZE}-byte reports)...")

try:
    while True:
        readable, _, _ = select.select([fd], [], [])
        if not readable:
            continue

        try:
            data = os.read(fd, REPORT_SIZE)
        except BlockingIOError:
            continue

        if not data:
            continue

        print(f"Received {len(data)} bytes: {data.hex(' ')}")

finally:
    os.close(fd)
