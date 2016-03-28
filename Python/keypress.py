"""keypress - a module for detecting a single keypress."""

try:
    import msvcrt

    def getkey():
        """wait for a keypress and return a single char string."""
        return msvcrt.getch()
except ImportError:
    import sys
    import tty
    import termios

    def getkey():
        """wait for a keypress and return a single char string."""
        fd = sys.stdin.fileno()
        original_attributes = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, original_attributes)
        return ch
    # if either of the unix-specific tty or termios are not found
    # we allow importerror to propagate from here.

def main():
    print("'keypress' example starting... press a key")
    getkey()
    print("'keypress' example ending...you pressed a key")

if __name__ == '__main__':
    main()