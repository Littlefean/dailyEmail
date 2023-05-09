"""
机器人
"""
from random import choice, random


def main():
    if random() < 0.2:
        with open("functions/robotDiary/diary.txt", encoding="utf-8") as f:
            content = f.read().strip()
        arr = content.split()
        return choice(arr)
    else:
        return ""
