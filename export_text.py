from psd_tools import PSDImage
import translators as ts
import json
import os

# Выбор языка и переводчика
from_language = "en"
to_language = "ru"
translator = "yandex"


# Получаем путь к папке "input"
input_directory = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Input")
# Проверяем, существует ли папка "Input", если нет - создаем
if not os.path.exists(input_directory):
    os.makedirs(input_directory)
    print(f"Папка '{input_directory}' была создана.")

# Ищем все файлы с расширением .psd в папке "Input"
psd_files = [f for f in os.listdir(input_directory) if f.endswith(".psd")]

# Проверяем количество найденных файлов
if len(psd_files) == 0:
    print("Нет необходимого файла .psd в папке 'input'.")
    exit(0)
elif len(psd_files) > 1:
    print("Должен быть только один файл .psd в папке 'input'.")
    exit(0)
else:
    print(f"Найден файл: {psd_files[0]}")


def extract_and_translate_text(psd_file):
    """Проходит по слоям PSD, извлекает текст и переводит его."""

    # Формируем полный путь к файлу
    psd_path = os.path.join(input_directory, psd_file)

    # Загружаем PSD файл
    psd = PSDImage.open(psd_path)
    translated_texts = {}

    # Рекурсивная функция для поиска текстовых слоев
    def process_layers(layers):
        for layer in layers:
            # Если слой - это группа (папка), рекурсивно обрабатываем её содержимое
            if layer.is_group():
                process_layers(layer)

            if layer.kind == "type":  # Проверяем, текстовый ли слой
                original_text = layer.text
                if original_text:
                    try:
                        # Перевод текста с помощью Yandex или другого переводчика
                        translated_text = ts.translate_text(
                            original_text,
                            from_language=from_language,
                            to_language=to_language,
                            translator=translator,
                        )

                        if translated_text:  # Проверяем, что перевод успешен
                            # Сохраняем переведенный текст
                            translated_texts[original_text] = translated_text
                        else:
                            print(
                                f"Ошибка: не удалось перевести текст: '{original_text}'"
                            )
                    except Exception as e:
                        print(f"Ошибка при переводе текста '{original_text}': {str(e)}")

    # Обрабатываем все слои PSD
    process_layers(psd)

    return translated_texts


# Пример использования
if psd_files[0] is not None:
    translated_texts = extract_and_translate_text(psd_files[0])

    # Получаем путь к папке "Output"
    output_directory = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "Output"
    )
    # Проверяем, существует ли папка "Output", если нет - создаем
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Папка '{output_directory}' была создана.")

    # Полный путь для сохранения
    file_path = os.path.join(output_directory, "translated_text.json")

    # Сохраняем переведенный текст в JSON файл
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(translated_texts, f, ensure_ascii=False, indent=4)

    print("Переведенный текст сохранен в 'Output'")
    print(
        "Далее укажите в import_text.jsx путь до созданного файла json '/Output/translated_text.json'"
    )
