import asyncio
from edge_tts import Communicate
import os

# 参数输入
async def text_to_speech(text, output_file):
    communicate = Communicate(text, "en-US-AvaNeural", rate="+25%")
    await communicate.save(output_file)
    print(f"Saved: {output_file}")

# 在这里指定输入的文件。
def main():
    input_file = "INtts.txt"
    with open(input_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

# 将会自动创建output文件夹，内部文件会被覆盖，确保该文件夹下没有文件。
# 保存格式out_#.wav。
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue
        output_file = f"out_{i+1}.wav"
        asyncio.run(text_to_speech(line, output_file))

if __name__ == "__main__":
    main()