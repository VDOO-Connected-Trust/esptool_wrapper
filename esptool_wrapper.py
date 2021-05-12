#!/usr/bin/env python3
import os
import argparse

from esptool import LoadFirmwareImage


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", type=str, help="Espressif image file path")
    parser.add_argument("-o", "--output_path", type=str, help="Segments output path")
    args = parser.parse_args()

    input_path = args.input_path
    segments_dir = args.output_path

    appimage = LoadFirmwareImage('esp32', input_path)
    for segment in appimage.segments:
        segment_properties = [seg_range[2] for seg_range in appimage.ROM_LOADER.MEMORY_MAP
                              if seg_range[0] <= segment.addr < seg_range[1]]
        segment_path = os.path.join(segments_dir, f'{os.path.basename(input_path)}_{segment.addr:0x}')
        # todo: Parse segments according properties
        print(f'dd segment between {segment.addr} and {segment.addr + len(segment.data)} to ' +
              f'{segment_path} - {segment_properties}')
        with open(segment_path, 'wb') as file:
            file.write(segment.data)


if __name__ == '__main__':
    main()
