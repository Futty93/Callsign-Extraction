import whisper
from whispercpp import Whisper
import pyaudio
import wave
import time
import keyboard
from main import extraction_flight_number as main

def record(w):
    # 録音の設定
    chunk = 1024  # 1度に読み込むデータ量
    sample_rate = 44100  # サンプリングレート
    channels = 1  # チャンネル数

    # 録音フラグ
    is_recording = False

    # 録音データ
    data = []
    
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
            filepath = f"./record_files/{filename}"

            # WAVファイルを開く
            wf = wave.open(filepath, 'wb')
            wf.setnchannels(channels)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)

            print("録音を開始しました...")

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
            print(main(text[0]))

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