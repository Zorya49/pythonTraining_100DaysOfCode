from gtts import gTTS
import pypdf

LANGUAGE = 'en'

file_name = input("Type name of pdf file that you want to convert to speech (without extension)\n")

reader = pypdf.PdfReader(f'{file_name}.pdf')
pages_count = len(reader.pages)
parts = []

for i in range(pages_count):
    try:
        page = reader.pages[0]
        parts.append(page.extract_text())
    except:
        pass

text = " ".join(parts)

print("The file is processed...")
speech = gTTS(text=text, lang=LANGUAGE, slow=False)
speech.save(f'{file_name}.mp3')
