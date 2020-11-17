from PIL import Image
import pytesseract
import argparse
import cv2
import os
import re
from pynput import keyboard
from pynput.keyboard import Key, Controller
from directKeys import left_click
import time
from params import *
from PIL import ImageGrab
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from unidecode import unidecode
from datetime import datetime
break_program = False


def on_press(key):
    global break_program

    print(key)
    if key == keyboard.Key.space:
        print('end pressed')
        break_program = True
        return False


def reset_cursor():
    for _ in range(20):
        left_click(reset_cursor_pos[0], reset_cursor_pos[1], sleep_time=0.1)


def open_hdv(pos_vendeur):
    left_click(pos_vendeur[0], pos_vendeur[1])
    time.sleep(0.2)
    left_click(pos_vendeur[0] + 40, pos_vendeur[1] + 90)
    time.sleep(0.5)
    reset_cursor()


def get_price(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # scale_percent = 150
    #
    # width = int(gray.shape[1] * scale_percent / 100)
    # height = int(gray.shape[0] * scale_percent / 100)
    #
    # dsize = (width, height)
    #
    # gray = cv2.resize(gray, dsize)
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(filename), lang='eng',
                                       config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')
    os.remove(filename)

    text = text.split('\n')
    return text[0]


def get_name(img):
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)

    ret, thresh4 = cv2.threshold(gray, 139, 255, cv2.THRESH_TOZERO)

    ret, thresh4 = cv2.threshold(thresh4, 0, 255, cv2.THRESH_TOZERO)
    thresh4 = cv2.GaussianBlur(thresh4, (3, 3), 0)

    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, thresh4)

    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    text = pytesseract.image_to_string(Image.open(filename), config='--psm 11')
    os.remove(filename)

    # cv2.imshow('input', img)
    # cv2.imshow('thresh4', thresh4)
    # cv2.waitKey(0)
    #
    text = text.split('\n')
    text = [i for i in text if i is not '' and i is not ' ']

    return text


def scan_hdv(pos_vendeur, nb_ressources, price_df):
    open_hdv(pos_vendeur)

    ressources_range = 4 if pos_vendeur == vendeur_ressources[:2] else 1

    for j in range(ressources_range):
        for i in range(nb_ressources):
            obj_type = ImageGrab.grab(bbox=obj_type_crop)
            obj_type = get_name(np.asarray(obj_type))[0]
            reset_cursor()
            screen = ImageGrab.grab(bbox=screen_crop)

            while screen.getpixel((825 - screen_crop[0], 660 - screen_crop[1])) != (
                    81, 74, 60) and not break_program:
                screen = ImageGrab.grab(bbox=screen_crop)
                prices = []
                name_img_crop = ImageGrab.grab(bbox=name_crop)
                names = get_name(np.asarray(name_img_crop))
                print(names)
                for k in range(len(names) - 1):
                    if break_program:
                        break
                    left_click(380, 280 + k * 35)
                    time.sleep(0.2)
                    price_img_crop_x1 = ImageGrab.grab(bbox=first_price_crop_x1)
                    price_x1 = get_price(np.asarray(price_img_crop_x1))

                    price_img_crop_x10 = ImageGrab.grab(bbox=first_price_crop_x10)
                    price_x10 = get_price(np.asarray(price_img_crop_x10))

                    price_img_crop_x100 = ImageGrab.grab(bbox=first_price_crop_x100)
                    price_x100 = get_price(np.asarray(price_img_crop_x100))

                    prices.append((price_x1, price_x10, price_x100))
                    print(price_x1, price_x10, price_x100)

                for name, price in zip(names, prices):
                    price_df = price_df.append({'type': str(obj_type),
                                                'name': unidecode(str(name)).lower(),
                                                '1x': int(price[0]) if price[0].isnumeric() else None,
                                                '10x': int(price[1]) if price[1].isnumeric() else None,
                                                '100x': int(price[2]) if price[2].isnumeric() else None},
                                               ignore_index=True)
                left_click(825, 660)
                time.sleep(0.3)

                if screen.getpixel((825 - screen_crop[0], 660 - screen_crop[1])) != (190, 185, 152):
                    break

            left_click(530, 224)
            time.sleep(0.2)
            if j == 0:
                if i == nb_ressources - 1:
                    break
                left_click(530, 224 + ((i + 2) * 35))
                time.sleep(0.2)
            elif j == 1:
                left_click(787, 577)
                time.sleep(0.2)
                left_click(530, 224 + ((i + 5) * 35))
                time.sleep(0.2)
                if i + 5 > nb_ressources:
                    break
            elif j == 2:
                left_click(787, 577)
                time.sleep(0.2)
                left_click(787, 577)
                time.sleep(0.2)
                left_click(530, 224 + ((i + 5) * 35))
                time.sleep(0.2)
                if i + 5 > nb_ressources:
                    break
            elif j == 3:
                left_click(787, 577)
                time.sleep(0.2)
                left_click(787, 577)
                time.sleep(0.2)
                left_click(787, 577)
                time.sleep(0.2)
                left_click(530, 224 + ((i + 10) * 35))
                time.sleep(0.2)
                if i + 9 > nb_ressources:
                    break

            if break_program:
                break

        if break_program:
            break

    return price_df


def change_HDV(pos_transpo, pos_in_list):
    keyboard = Controller()
    keyboard.press(Key.esc)
    keyboard.release(Key.esc)
    time.sleep(1)
    left_click(pos_transpo[0], pos_transpo[1])
    time.sleep(1)
    left_click(pos_transpo[0] + 50,  pos_transpo[1] + 60)
    time.sleep(0.3)
    left_click(pos_HDV_onglet[0], pos_HDV_onglet[1])
    time.sleep(0.3)
    left_click(pos_HDV_onglet[0], 258 + pos_in_list * 45)
