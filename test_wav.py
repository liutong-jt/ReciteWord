import wave

# 指定 WAV 文件路径
wav_file_path = r'Sounds\WsFinish.wav'

# 打开 WAV 文件
with wave.open(wav_file_path, 'rb') as wave_file:
    # 获取音频参数
    channels = wave_file.getnchannels()  # 声道数
    sample_width = wave_file.getsampwidth()  # 采样宽度（字节）
    framerate = wave_file.getframerate()  # 采样率
    num_frames = wave_file.getnframes()  # 音频帧数

    # 读取音频数据
    audio_data = wave_file.readframes(num_frames)

# 打印音频参数信息
print(f'Channels: {channels}')
print(f'Sample Width: {sample_width} bytes')
print(f'Frame Rate: {framerate} Hz')
print(f'Number of Frames: {num_frames}')

# 处理音频数据，这里只是打印前 10 个采样值
samples = list(audio_data)[:10]
print(f'Samples: {samples}')
