from main import main as main
import json
import re

from whispercpp import Whisper

w = Whisper('small')
import os
import json

if __name__ == "__main__":
    # 入力ディレクトリのパス
    input_dir = "../../修論/狩川先生読み上げ音声/抽出失敗"
    # 出力ファイルのパス
    output_file = "/Users/futawatari/Downloads/ATC_text_Fail_output.json"

    # 結果を格納するリスト
    output_data = []

    # 入力ディレクトリ内のすべての.m4aファイルを取得
    m4a_files = [os.path.join(input_dir, file) for file in os.listdir(input_dir) if file.endswith(".m4a")]

    # 各.m4aファイルに対して処理を実行
    for file_path in m4a_files:
        try:
            print(f"Processing file: {file_path}")
            # 音声ファイルの文字起こし結果を取得
            result = w.transcribe(file_path)
            text = w.extract_text(result)

            # 結果をリストに格納
            output_data.append({
                "file": file_path,
                "transcription": text
            })
        except Exception as e:
            print(f"Error processing file {file_path}: {e}")

    # 結果を新しいJSONファイルに書き出す
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=4)

    print(f"Processed data saved to {output_file}")
    