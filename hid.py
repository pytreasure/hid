# Core code of HID.
# Build commands for HID keyboard and mouse.

hidCom = None


def set_com(which_com):
    global hidCom
    hidCom = which_com


def keyboard(keys, delay):
    if hidCom is None:
        return
    commands = {

    }
    keys_type = type(keys)
    if keys_type == "number":
        keys_type = str(keys_type)
    if keys_type == "list" or keys_type == "tuple":
        keys_type = 1
    elif keys_type == "string":
        keys_type = 2
    else:
        return ()


def mouse(keys):
    commands = {

    }
    keys_type = type(keys)
    if keys_type == "number":
        keys_type = str(keys_type)
    if keys_type == "list" or keys_type == "tuple":
        keys_type = 1
    elif keys_type == "string":
        keys_type = 2
    else:
        return ()
