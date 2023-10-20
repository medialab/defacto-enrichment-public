from src.constants import CONFIG, MINALL_OUTPUT


def cleanup():
    # Remove written config file, which was given to minall
    CONFIG.unlink()

    # Remove minall's output directory
    [file.unlink() for file in MINALL_OUTPUT.iterdir()]
    MINALL_OUTPUT.rmdir()
