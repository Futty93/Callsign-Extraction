word_register.json: 音声文字起こしの結果から探したい単語をあらかじめ登録しておく。コールサインなど

airline_code_dict: コールサインがキー、3レターコードがvalueの辞書型。空域情報に合わせてあらかじめ登録が必要

word_metaphone_key.json: word_register.jsonをもとにgenerate_word_metaphone_key.pyから生成される

sentenceFormat.py: 入力された文章から",", ".", "'", "-"を削除し、s数字が連続している場合にはその間にあるスペースを削除する 

metaphone.py: フォーマット済みの文章を受け取り、各単語に対応するmetaphoneKeyを配列で返す

