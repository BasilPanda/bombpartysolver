import cv2
import numpy as np
import time
import pytesseract
from PIL import ImageGrab
import keyboard

filepath_words = "dict\\dict.txt"
input_coords = [736, 1371, 1455, 1414]
letter_coords = [2059, 197, 2181, 1339]
bomb_coords = [1057, 759, 1123, 803]
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
all_words = []


def main():
    used = []
    # temp = 0
    while True:
        cap_input_box = np.array(ImageGrab.grab(bbox=input_coords))
        cap_input_box = cv2.cvtColor(cap_input_box, cv2.COLOR_BGR2GRAY)
        cap_letters = np.array(ImageGrab.grab(bbox=letter_coords))
        cap_letters = cv2.cvtColor(cap_letters, cv2.COLOR_BGR2GRAY)
        cap_bomb = np.array(ImageGrab.grab(bbox=bomb_coords))
        cap_bomb = cv2.cvtColor(cap_bomb, cv2.COLOR_BGR2GRAY)
        # 20 is when it's current turn to input
        if cap_input_box[750 - input_coords[0], 1380 - input_coords[1]] == 20:
            # run function
            text = pytesseract.image_to_string(cap_bomb)
            #print(text)

            thresh = 255 - cv2.threshold(cap_bomb, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]

            # thresh = cv2.GaussianBlur(thresh, (3, 3), 0)
            data = pytesseract.image_to_string(thresh, lang='eng', config='--psm 7 -c tessedit_char_whitelist'
                                                                          '=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
            letters = data.rstrip().lower()
            print(letters)
            if letters.isalpha():
                # if 20 >= cap_input_box[750 - input_coords[0], 1380 - input_coords[1]]:
                    # print(f"Int: {cap_input_box[750 - input_coords[0], 1380 - input_coords[1]]}")
                    # temp = cap_input_box[750 - input_coords[0], 1380 - input_coords[1]]
                valid = getValid(letters)

                # Get the best word possible that isn't already used
                best = findLongestUnique(valid, used)

                used.append(best)
                print(best)
                keyboard.write(best)
                keyboard.press_and_release('enter')
            time.sleep(0.25)
            # text = pytesseract.image_to_string(cap_letters)
            # print(text)

            # Shows the capture of the bomb
            # cv2.imshow("thresh", thresh)
            # Wait
            time.sleep(1)

        if cv2.waitKey(1) == 27:
            break
        # 1440p monitor
        # input box
        # x736 y1371
        # x1455 y1414

        # letters on right
        # x2059 y197
        # x2181 y1339

        # words in middle
        # x1057 y759
        # x1123 y803
    cv2.destroyAllWindows()


def loadWords():
    with open(filepath_words, "r") as f:
        for line in f:
            all_words.append(line.rstrip().lower())


def getValid(letters):
    valid = []
    for word in all_words:
        if letters in word:
            valid.append(word)
    return valid


def findLongestUnique(words, used):
    longest = ""
    for word in words:
        if word in used:
            continue
        if len(set(word)) > len(set(longest)):
            longest = word
            used.append(word)
    return longest


if __name__ == "__main__":
    loadWords()
    main()
