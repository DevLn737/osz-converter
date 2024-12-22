import os
import shutil
import concurrent.futures
import platform
import ctypes


def convert(beatmapset_path, output_folder):
    archive_name = os.path.basename(beatmapset_path)  # Имя архива без пути
    archive_path = os.path.join(output_folder, archive_name + ".osz")  # Полный путь к .osz файлу

    # Пропуск, если файл уже существует
    if os.path.exists(archive_path):
        print(f"Skipped: {archive_name} already exists.")
        return

    # Проверка, что это директория
    if not os.path.isdir(beatmapset_path):
        print(f"Skipped: {beatmapset_path} is not a directory.")
        return

    try:
        # Создание временного ZIP-архива
        temp_zip_path = shutil.make_archive(os.path.join(output_folder, archive_name), "zip", beatmapset_path)

        # Переименование в .osz
        os.rename(temp_zip_path, archive_path)

        print(f"Successfully converted: {archive_name}")
    except PermissionError as e:
        print(f"Permission error: {beatmapset_path}. Details: {e}")
    except OSError as e:
        print(f"OS error while processing {beatmapset_path}. Details: {e}")
    except Exception as e:
        print(f"Unexpected error during processing {beatmapset_path}. Details: {e}")


def convert_all(songs_path, output_folder):
    beatmapsets = [
        f for f in os.listdir(songs_path) if os.path.isdir(os.path.join(songs_path, f))
    ]

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {
            executor.submit(
                convert, os.path.join(songs_path, beatmapset), output_folder
            ): beatmapset
            for beatmapset in beatmapsets
        }

        for future in concurrent.futures.as_completed(futures):
            beatmapset = futures[future]
            try:
                future.result()
            except PermissionError as e:
                print(f"Access rights error {beatmapset}: {e}")
            except Exception as e:
                print(f"Error during processing {beatmapset}: {e}")


def main():
    while True:
        osu_folder = input("Path to the osu folder: ").strip()
        output_folder = input("Path to the output folder (leave empty for default): ").strip()

        if not output_folder:
            output_folder = os.path.join(osu_folder, "songs_processed")
            os.makedirs(output_folder, exist_ok=True)
            print(f"Output folder not specified. Created: {output_folder}")
        elif not os.path.exists(output_folder):
            os.makedirs(output_folder)
            print(f"Output folder created: {output_folder}")

        if os.path.exists(osu_folder) and os.path.exists(output_folder):
            osu_songs_path = os.path.join(osu_folder, "Songs")
            print(f"Folders are confirmed:\n{osu_songs_path}\n{output_folder}")
            break
        else:
            print("Wrong path, Try again.")

    convert_all(osu_songs_path, output_folder)


def is_admin():
    """
    Проверяет, запущена ли программа от имени администратора (или root).
    :return: True, если администратор (root), иначе False.
    """
    target_platform = platform.system()

    if target_platform in {"Linux", "Darwin"}:
        return os.getuid() == 0

    if target_platform == "Windows":
        try:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        except AttributeError:
            print("Error: Unable to check admin rights")
        except Exception as e:
            print(f"Unexpected error while checking admin rights: {e}")
        return False


if __name__ == "__main__":
    if is_admin():
        main()
    else:
        print("Run as administrator...")
        input()
