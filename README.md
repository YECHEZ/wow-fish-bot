# wow-fish-bot
## WoW Vanilla fish bot. Python, simple, for me. World of Warcraft 1.12.1
- No hook sounds, work with all resolution.
- Using opencv2, PIL, pyautogui, numpy, keyboard, win32gui
- code = 92 lines with spaces.

How to:
1. Equip fishing pole
2. Move skill 'Fishing' to slot with bind '1'
3. Hide UI (ALT + Z)
4. Full camera zoom
5. Run bot

- Stop/Start key = ']' / Default as Start
- Work only if found active window 'World of Warcraft'
- How it work: 
> With cv2 the bot tracks the splashes on water and clicks into the point via LeftShift + RMB
* Bot has false positives because simple
- Best performance on 800x600 Windowed Mode, no maximized
or 1920x1080 maximized

- Tested on areas: Orgrimmar, near WC dungeon and Ratchet
- Works pretty normal (80%)
- Gif - https://imgur.com/a/IRftPyX
![alt text](wow-fish-bot-area.png)
