# import whisper
from whispercpp import Whisper
import pyaudio
import wave
import time
import keyboard
from main import extraction_flight_number as extractor
from API.send_highlight_aircraft import highlight_aircrafts
import os
import json

def record(w):
    # # transcription_results.jsonの読み込み
    # results_filepath = "./record_files/transcription_results.json"

    # ATCの模擬スクリプト読み上げ用のディレクトリ
    results_filepath = "./ATC_test_recording/transcription_results.json"

    if os.path.exists(results_filepath):
        with open(results_filepath, 'r', encoding='utf-8') as f:
            results = json.load(f)
    else:
        results = []

    # 録音の設定
    global stream, filepath, start_time, wf, filename
    chunk = 1024  # 1度に読み込むデータ量
    sample_rate = 44100  # サンプリングレート
    channels = 1  # チャンネル数

    # 録音フラグ
    is_recording = False

    # 録音データ
    data = []
    
    # 抽出したコールサインを格納
    extracted_callsigns = [['SKY514', 2]]
    
    print("Recording is available...")

    while True:
        # Shiftキーが押されているかどうか
        is_shift_pressed = keyboard.is_pressed('shift')

        # 録音開始
        if not is_recording and is_shift_pressed:
            is_recording = True
            start_time = time.time()

            # ストリームの作成
            stream = pyaudio.PyAudio().open(format=pyaudio.paInt16,
                                             channels=channels,
                                             rate=sample_rate,
                                             input=True,
                                             frames_per_buffer=chunk)

            # ファイルパス生成
            filename = f"recording_{int(start_time)}.wav"

            # ファイルパス生成
            filepath = f"./ATC_test_recording/{filename}"

            # WAVファイルを開く
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)

            print("録音を開始しました...")
            
            highlight_aircrafts(extracted_callsigns, "NO_VALUE") # コールサインのハイライトをリセット
            

        # 録音中
        if is_recording:
            data.append(stream.read(chunk))

        # 録音終了
        if is_recording and not is_shift_pressed:
            is_recording = False
            end_time = time.time()
            recording_time = end_time - start_time

            # WAVファイルへの書き込み
            wf.writeframes(b''.join(data))
            wf.close()

            print(f"録音を終了しました。録音時間: {recording_time:.2f}秒")

            result = w.transcribe(filepath)
            text = w.extract_text(result)
            print(text)

            # 短いテキストの場合は処理をスキップしてファイルを削除
            if len(text[0]) <= 10 or text[0][1] == "[":
                print(f"{filename} is too short, skipping and deleting file.")
                os.remove(filepath)
                continue

            extracted_callsigns = extractor(text[0])

            print(extracted_callsigns)

            # transcription_results.jsonにデータを追加
            results.append({
                "file_name": filename,
                "transcription": text,
                "extracted_callsign": extracted_callsigns
            })

            # JSONファイルの更新
            with open(results_filepath, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=4)

            highlight_aircrafts(extracted_callsigns, "SUCCESS")  # コールサインのハイライトを更新

            # データ初期化
            data = []

        # Escキーが押されたら終了
        if keyboard.is_pressed('esc'):
            break

    # ストリーム (存在する場合) を停止
    if stream:
        stream.stop_stream()
        stream.close()

    print("プログラムを終了します。")
    
    
if __name__ == '__main__':
    w = Whisper('small')
    record(w)