"""
Simulates a Skylanders Portal of Power

Based on Martin Kneppers' article: https://marijnkneppers.dev/posts/reverse-engineering-skylanders-toys-to-life-mechanics/
And GamerBross' commit here: https://github.com/cemu-project/Cemu/commit/33d5c6d
Created by Anthony Guy 2026
"""

def log_packet(direction: str, packet: bytes):
    print(f"{direction}: {packet.hex(' ')}")

class SkylandersPortal:
    """Standard Skylanders Portal"""
    VENDOR_ID = 0x1430  # Activision device

    PRODUCT_ID = 0x1F17  # X360 Giants portal (?)

    COMMAND_SIZE = 32  # Skylanders portal data size
    REPORT_SIZE = 64  # USB protocol data size

    CMD_READY = ord("R")  # 0x52, READY command

    def handle_command(self, command: bytes) -> bytes:
        """Process a command and reply"""

        if not command:  # NULL command
            return bytes(self.COMMAND_SIZE)

        command_type = command[0]

        if command_type == self.CMD_READY:  # READY command
            return self.handle_ready()

        return bytes(self.COMMAND_SIZE)

    def handle_ready(self) -> bytes:
        """Build ready command"""
        response = bytearray(self.COMMAND_SIZE)

        response[0] = self.CMD_READY
        response[1] = 0x02
        response[2] = 0x1B

        return bytes(response)

    #@staticmethod
    #def parse_command(data: bytes):
    #    """Extract the command char from a 32-byte packet"""
    #    if len(data) != 32:
    #        raise ValueError(f"[parse_command] ERR: Commands should be 32 bytes long, got {len(data)} bytes!")
    #    return chr(data[0])

    # def ready_response(byte1: int, byte2: int):
    #    if not 0 <= byte1 <= 0xFF:
    #        raise ValueError(f"[READY_RESPONSE] ERR: byte 1 must be between 0x00 and 0xFF, got {byte1}!")

    #def make_command(self, command: str) -> bytes:
    #    """Create a 32-byte command packet"""
    #    if len(command) != 1 or not command.isascii():
    #        raise ValueError(f"[make_command] ERR: Commands should be a single ASCII character, got \"{command}\"!")
    #    return command.encode("ascii") + bytes(self.COMMAND_SIZE - 1)

class Xbox360Portal(SkylandersPortal):
    """Xbox 360 specific portal translation"""

    HEADER = bytes([0x0B, 0x14])  # Prefixes all commands

    def wrap(self, report: bytes) -> bytes:
        """Append custom xbox header to report"""
        return self.HEADER + report

    def unwrap(self, report: bytes) -> bytes:
        """Check validity and strip xbox header from report"""

        if not report.startswith(self.HEADER):  # Check the header is correct
            raise ValueError(f"[unwrap] ERR: Invalid Xbox360 header. Expected: '{self.HEADER}', Received: '{report[:2].hex(' ')}'")

        return report[2:]  # Strip xbox header into normal portal communication

    def handle_report(self, report: bytes) -> bytes:
        """Translate xbox portal to universal protocol"""
        command = self.unwrap(report)

        response = self.handle_command(command)

        return self.wrap(response)

class PortalState:
    """Current emulated state of a portal"""
    isActivated = False


if __name__ == "__main__":  # Run tests
    portal = Xbox360Portal()

    test_request = bytes([0x0B, 0x14, ord("R")]) + bytes(SkylandersPortal.COMMAND_SIZE - 3)  # Request from Xbox360

    test_response = portal.handle_report(test_request)

    print(test_response.hex(' '))
