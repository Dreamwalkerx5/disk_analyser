#  Copyright (c) 2019. Steven Taylor All rights reserved


def pad_string(text='', length=0, pad_char='', back=True):
    padding = length - len(text)
    if padding >= 0:
        if back:
            text += pad_char * padding
        else:
            text = (pad_char * padding) + text
    else:
        text = text[:length]

    return text
