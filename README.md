# GBFR-AutoTrading
Auto trading Wrightstones or Sigils with Siero
# Guideline
Module versions perhaps don't matter, since they are less related.
```bash
pip install opencv-python
pip install easyocr
pip install numpy
pip install pyautogui
pip install pynput
pip install keyboard
```
Somehow this program doesn't work as I expected (run 24/7 until you sell all useless wrightstones and sigils), it will automatically stop operating after 30 minutes. Nevertheless, you can still sell some useless items for a while (you have to manually restart per 30 minutes).
1. there are 3 list in lines 30 - 40, you may have to do some changes: banList (sell them no matter what their 2nd trait is), conditional_ban (sell them if their 2nd trait is in "banList_trait", meaning that such sigils are not worth keeping given their second trait is trash), banList_trait (useless traits).
2. Each time you run this program can only choose either selling wrightstones or sigils, check line 499
3. Set the game language to English, resolution = 1080p (both ingame and windows setting)
4. Find Siero and press F once
5. Run autoSell.py
6. Press P to stop
