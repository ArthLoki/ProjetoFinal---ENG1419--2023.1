from generateVoiceFromText_tts import text2voice


def run():
    prompt = "Diga 'Olá mundo'"
    character = 'robo'

    text2voice(prompt, character)

    return

run()