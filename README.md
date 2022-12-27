# Usage

1. Make sure you have Python and Pip installed.

2. Open the command prompt and enter the command `pip install -r requirements.txt` and run it.

3. Place the images you want to process in a folder called "input" in the root directory of the project.

4. Run `main.py` and wait for the program to process your files.

5. Done, the processed files will be placed in a folder called "output" in the root directory of the project.

# Parameter Settings

You can adjust the program parameters by editing the contents of `config.json`.

The following is a description of the adjustable parameters:

1. `target-color`: Must be an array of RGBA values, this is the background color that needs to be replaced, the default value is white.

2. `tolerance`: Must be a number between 0 and 1, similar colors to `target-color` will also be replaced when replacing the background, the higher the value, the greater the difference that can be accepted, the value of 0 means only accept colors that match `target-color` exactly, the value of 1 means accept any color, the default value is 0.05.

---

# 使用方法

1. 確保您已安裝 Python 和 Pip 。

2. 打開命令提示符 (command prompt) 輸入指令 `pip install -r requirements.txt` 並運行。

3. 將您要處理的圖片放入專案根目錄中名為 input 的文件夾。

4. 運行 `main.py`，等待程序處理您的文件。

5. 完成，處理後的文件會放入專案根目錄中名為 output 的文件夾。

# 參數設置

您可以通過編輯 `config.json` 中的內容調整程序參數。

以下是可以被調整的參數的描述：

1. `target-color`: 必需是一個 RGBA 值的數組，這是需要被取代的背景顏色，默認值為白色。

2. `tolerance`: 必需是介於 0 到 1 的數字，替換背景的時候也會替換 `target-color` 的相近顏色，數值越高表示能夠接受的差別更大，數值為 0 表示只接受與 `target-color` 完全相符的顏色，數值為 1 表示接受任何顏色，默認值為 0.05。

---

BY CCH137