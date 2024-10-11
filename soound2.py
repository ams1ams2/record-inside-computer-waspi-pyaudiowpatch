import pyaudiowpatch as pyaudio
import wave

# إنشاء كائن PyAudio
p = pyaudio.PyAudio()

# البحث عن جهاز WASAPI loopback
loopback_device_index = None
for i in range(p.get_device_count()):
    device_info = p.get_device_info_by_index(i)
    if device_info["name"].lower().find("loopback") != -1:
        loopback_device_index = i
        break

if loopback_device_index is None:
    raise Exception("WASAPI loopback device not found")

# الحصول على معدل العينة المدعوم من الجهاز
device_info = p.get_device_info_by_index(loopback_device_index)
supported_sample_rate = int(device_info["defaultSampleRate"])
print(f"Using supported sample rate: {supported_sample_rate}")

# إعداد للتسجيل باستخدام معدل العينة المدعوم
stream = p.open(format=pyaudio.paInt16,
                channels=2,
                rate=supported_sample_rate,
                input=True,
                input_device_index=loopback_device_index,
                frames_per_buffer=1024)

print("Recording from WASAPI Loopback...")

frames = []

# تسجيل الصوت لمدة 5 ثوانٍ
for _ in range(0, int(supported_sample_rate / 1024 * 5)):
    data = stream.read(1024)
    frames.append(data)

print("Finished recording.")

# إغلاق التدفق
stream.stop_stream()
stream.close()
p.terminate()

# حفظ الملف الصوتي المسجل
wf = wave.open("output_loopback.wav", 'wb')
wf.setnchannels(2)  # قناة استيريو (2 قنوات)
wf.setsampwidth(p.get_sample_size(pyaudio.paInt16))
wf.setframerate(supported_sample_rate)
wf.writeframes(b''.join(frames))
wf.close()

print("Saved to output_loopback.wav")
