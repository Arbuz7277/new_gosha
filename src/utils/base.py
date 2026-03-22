import time

def cent_to_coin(cent):
    return str(round(cent / 100, 2)).replace('.', ',')