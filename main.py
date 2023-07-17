import os
import shutil
import concurrent.futures
from utils import measure_time


def convert(beatmapset_path, output_folder):
    archive_path = os.path.join(output_folder, os.path.basename(beatmapset_path))

    if os.path.exists(archive_path + ".osz"):
        return
    shutil.make_archive(archive_path, 'zip', beatmapset_path)
    os.rename(archive_path + ".zip", archive_path + ".osz")
    print(os.path.basename(beatmapset_path))


@measure_time
def convert_all(songs_path, output_folder):
    beatmapsets = os.listdir(songs_path)

    with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = []
        for beatmapset in beatmapsets:
            beatmapset_path = os.path.join(songs_path, beatmapset)
            output_path = output_folder
            future = executor.submit(convert, beatmapset_path, output_path)
            futures.append(future)


def main():
    while True:
        osu_folder = input("Path to the osu folder: ") + "\\Songs"
        output_folder = input(str("Path to the output folder: "))
        if os.path.exists(osu_folder) or os.path.exists(output_folder):
            print(osu_folder + "\n" + output_folder)
            break
        else:
            print("Неверный путь")
    convert_all(osu_folder, output_folder)


if __name__ == '__main__':
    main()
