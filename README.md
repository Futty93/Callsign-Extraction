## プロジェクト概要

このプロジェクトでは、`./registered_json` ディレクトリ内の `airline_code_dict.json` と `word_register.json` の2つのJSONファイルにコールサインを追加します。`airline_code_dict.json` では、コールサインは [callsign: 3レターコード] の形式で辞書として追加されます。`word_register.json` では、コールサインが複数の単語から構成される場合にも個別に追加されます（例: "all nippon", "all", "nippon"）。

JSONファイルを更新した後は、ターミナルで以下のコマンドを実行して、`requirements.txt` に記載されている依存関係をインストールする必要があります:

```bash
pip install -r requirements.txt
```
次に、registered_word_utils.py を実行して、registered_json ディレクトリに登録された情報から g2p および metaphone の辞書を生成します。生成された辞書は ./generated_json ディレクトリに保存されます。
```bash
python registered_word_utils.py
```

`main.py`の`main()`に文字起こしの結果の文章を渡して実行するとコールサインが抽出できた場合はコールサインが配列で、
できなかった場合には"Callsign not Found"と出力されます。


## Project Description
This project involves adding call signs to two JSON files, `airline_code_dict.json` and `word_register.json`, located in the `./registered_json` directory. In `airline_code_dict.json`, call signs are added in the format [callsign: 3-letter code] as a dictionary. In `word_register.json`, call signs are added individually, considering cases where a call sign consists of multiple words (e.g., "all nippon", "all", "nippon").

After updating the JSON files, you need to install the dependencies listed in `requirements.txt` by executing the following command in the terminal:

```bash
pip install -r requirements.txt
```
Next, you should run `registered_word_utils.py` to generate dictionaries for `g2p` and `metaphone` from the registered information in the `registered_json` directory. The generated dictionaries will be saved in the `./generated_json` directory.

```bash
python registered_word_utils.py
```
In `main.py`, the `main()` function accepts a transcribed text result as input. If call signs are found, they will be returned as an array. If no call signs are found, the output will be "Callsign not Found".

## 使用している外部ライブラリ
このプロジェクトでは、以下のライブラリとモジュールが使用されます:

- `json`: JSON ファイルの読み書きに使用されます。
- `doublemetaphone`: ダブルメタフォン（Double Metaphone）アルゴリズムを実装するライブラリです。
- `re`: 正規表現操作に使用されます。
- `G2p`: 英語の音素表現（Grapheme-to-Phoneme）変換を行うライブラリです。
- `Levenshtein.distance`: Levenshtein距離を計算するためのメソッドです。

これらのライブラリとモジュールは、プロジェクト内でテキストの処理、音素変換、および文字列の比較などのタスクに使用されます。



## External Libraries Used
This project utilizes the following libraries and modules:

- `json`: Used for reading and writing JSON files.
- `doublemetaphone`: A library implementing the Double Metaphone algorithm.
- `re`: Utilized for regular expression operations.
- `G2p`: A library for Grapheme-to-Phoneme conversion in English.
- `Levenshtein.distance`: Method for calculating Levenshtein distance.

These libraries and modules are used for tasks such as text processing, phonetic conversion, and string comparison within the project.