from datetime import datetime
from time import sleep
import os

try:
    from googletrans import Translator
    import yaml
except ImportError:
    print("""
You need to install googletrans and pyyaml to use this program.
> pip install googletrans==3.1.0a0
> pip install pyyaml
    """)
    os.system('pause')
    exit(1)

APP_NAME = 'Word Checker'
VERSION = '1.0.0'
AUTHOR = 'Manuel Cabral'
DEFAULT_CONFIG = {
    'source': 'es',
    'dest': 'en',
    'save': True,
    'attemps': 5
}


def gen_configs() -> dict:
    file = open('config.yml', 'w')
    yaml.dump(DEFAULT_CONFIG, file, sort_keys=False)
    file.close()
    return DEFAULT_CONFIG


def load_words() -> list:
    try:
        file = open('words.txt', 'r')
        data = file.readlines()
        if data is None:
            raise FileNotFoundError
        file.close()
        return data
    except FileNotFoundError:
        print('Words file not found or is empty, please create or fill it.')
        os.system('pause')


def load_configs() -> dict:
    try:
        file = open('config.yml', 'r')
        data = yaml.load(file, Loader=yaml.FullLoader)
        file.close()
        if data is None:
            print('Config file is empty, generating default config.')
            return gen_configs()
        return data
    except FileNotFoundError:
        print('Config file not found, generating one.')
        return gen_configs()


def check_config_keys(configs: dict) -> None:
    for key in DEFAULT_CONFIG.keys():
        if key not in configs.keys():
            print(f'Config not found: {key}')
            os.system('pause')
            exit(1)


def get_nouns(word, src, dest) -> list:
    translator = Translator()
    return translator.translate(
        word.strip(), src=src, dest=dest).extra_data['all-translations'][0][1]


def translating(word, attemps) -> list:
    print(f"""
Next word is: {word}
Max attempts: {attemps}
Type 'skip' or space to skip this word.
Type 'exit' to exit the program.

Starts in 3 seconds ..
    """)
    sleep(3)
    counter = 0
    translations = []
    while True:
        translation = input('Input: ')
        if translation == '' or translation == 'skip':
            break
        if translation == 'exit':
            return exit(1)
        counter += 1
        translations.append(translation)
        if counter == attemps:
            print('Max attempts reached, next word.')
            sleep(2)
            break
    return translations


def check_results(words, user_translations, wait_time, configs) -> None:
    for word in words:
        os.system('cls')
        print('Checking word:', word.strip())
        nouns = get_nouns(word, configs['source'], configs['dest'])
        total_nouns = len(nouns)
        user_translation = user_translations[word.strip()]
        print('Correct translations: ', nouns)
        print('Your translations: ', user_translation)

        counter = 0
        for user_translation in user_translation:
            if user_translation in nouns:
                nouns.remove(user_translation)
                counter += 1
        print(
            f'Points: {counter}/{total_nouns} with {configs["attemps"]} attempts.')
        sleep(wait_time)


def save_all(words, user_translations, configs):
    time = datetime.now().strftime('%d-%m-%Y_%H-%M-%S')
    print('Saving your translations ..')
    with open(file=f'{time}-your.yml', mode='w') as file:
        file.write(f'#{configs["source"]} to {configs["dest"]}\n')
        yaml.dump(user_translations, file, sort_keys=False)

    print('Saving correct translations ..')
    with open(file=f'{time}-correct.yml', mode='w') as file:
        file.write(f'#{configs["source"]} to {configs["dest"]}\n')
        for word in words:
            nouns = get_nouns(word, configs['source'], configs['dest'])
            yaml.dump({word.strip(): nouns}, file, sort_keys=False)


if __name__ == '__main__':
    configs = load_configs()
    check_config_keys(configs)
    os.system('cls')

    print(f"""
{APP_NAME} v{VERSION} by {AUTHOR}

Config file loaded ->
    Source language: {configs['source']}
    Destination language: {configs['dest']}
    Save translations: {configs['save']}
    Max attempts: {configs['attemps']}
""")
    words = load_words()
    print(f'Words file loaded -> {[word.strip() for word in words]}')

    print('Starting program in 5 seconds ..')
    sleep(5)
    user_translations = {}
    for word in words:
        os.system('cls')
        user_translations[word.strip()] = translating(word, configs['attemps'])

    os.system('cls')
    print('Program finished, checking your translations ..')
    sleep(2)

    nouns = check_results(words, user_translations, 10, configs)

    os.system('cls')

    if configs['save']:
        save_all(words, user_translations, configs)

    print('Finished, press any key to exit.')
    os.system('pause')
