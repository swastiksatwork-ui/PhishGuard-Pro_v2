import builtins

# Save the original print
_original_print = builtins.print


def stream_print(*args, **kwargs):
    # Convert everything to one string
    message = " ".join(str(arg) for arg in args)

    # TODO:
    # Later we'll send 'message' to the website here.
    _original_print("[INTERCEPTED]", message)

    # Still print normally to terminal
    _original_print(*args, **kwargs)


# Replace Python's print()
builtins.print = stream_print