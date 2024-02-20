import re

def sentence_format(text):
    # 不要な記号を削除
    text = text.replace(',', '').replace('.', '').replace("'", "").replace('"', '')

    # ハイフンをスペースに置換
    text = text.replace('-', ' ')
    # 数字と数字が連続している場合のスペースを削除する正規表現パターン
    pattern = re.compile(r'(\d+)\s+(\d+)')

    # パターンにマッチする箇所を探し、間のスペースを削除する
    modified_text = re.sub(pattern, r'\1\2', text)

    # もし修正されたテキストにパターンにマッチする部分があれば再度関数を呼び出す
    if modified_text != text:
        return sentence_format(modified_text)
    else:
        return modified_text
    