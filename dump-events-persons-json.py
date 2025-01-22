import os
import json
import hashlib
import shutil


def parse_contents_file(file_path):
    """Парсит файл contents.lr и возвращает данные в формате словаря."""
    data = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

        current_key = None
        current_value = []

        for line in lines:
            line = line.strip()

            if line == "---":
                if current_key is not None:
                    data[current_key] = "\n".join(
                        current_value) if current_key == "description" or current_key == "name" else current_value[0]

                current_key = None
                current_value = []
            elif current_key is not None:
                current_value.append(line)
            else:
                # Это новая пара ключ-значение
                key, value = line.split(":", 1)
                current_key = key.strip()
                current_value.append(value.strip())

        # Обработка последней записи, если она есть
        if current_key is not None:
            data[current_key] = "\n".join(current_value) if current_key == "description" or current_key == "name" else \
                current_value[0]

    return data


def get_image_hash(name):
    """Возвращает SHA-1 хэш имени."""
    return hashlib.sha1(name.encode('utf-8')).hexdigest()


def save_images(src_directory, dest_directory, name):
    """Сохраняет изображения в целевом каталоге с именами, основанными на SHA-1 хэше."""
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
    images = [f for f in os.listdir(src_directory) if f.lower().endswith(image_extensions)]

    if not images:
        return

    base_name = get_image_hash(name)
    for index, image in enumerate(images):
        # Создаем уникальное имя для изображения
        if index == 0:
            new_name = f"{base_name}{os.path.splitext(image)[1]}"
        else:
            new_name = f"{base_name}_{index + 1}{os.path.splitext(image)[1]}"

        # Полные пути к исходному и целевому файлам
        src_file_path = os.path.join(src_directory, image)
        dest_file_path = os.path.join(dest_directory, new_name)

        # Копируем файл в целевой каталог
        shutil.copy(src_file_path, dest_file_path)


def process_directory(directory):
    """Обрабатывает каталог и все его подкаталоги."""
    result = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file == "contents.lr" and root != 'events':
                file_path = os.path.join(root, file)

                data = parse_contents_file(file_path)
                result.append(data)

                # Сохраняем изображения в соответствующий каталог
                name = data.get("name", "unknown") if directory == "events" else data.get("fname",
                                                                                          "unknown") + " " + data.get(
                    "mname", "unknown") + " " + data.get("sname", "unknown")
                dest_directory = "events_data" if directory == "events" else "persons_data"

                # Создаем каталог назначения, если он не существует
                os.makedirs(dest_directory, exist_ok=True)

                # Сохраняем изображения
                save_images(root, dest_directory, name)

    return result


def main(input_directory):
    """Основная функция, которая запускает обработку."""
    if input_directory not in ["events", "persons"]:
        print("Укажите корректный каталог: 'events' или 'persons'.")
        return

    result_data = process_directory(input_directory)

    # Сохраняем результат в JSON файл
    output_file = f"{input_directory}_data.json"
    with open(output_file, 'w', encoding='utf-8') as json_file:
        json.dump(result_data, json_file, ensure_ascii=False, indent=4)

    print(f"Данные успешно сохранены в файл: {output_file}")


# Пример использования
if __name__ == "__main__":
    input_dir = input("Введите каталог (events или persons): ")
    main(input_dir)
