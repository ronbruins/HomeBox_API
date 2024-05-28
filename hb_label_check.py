import os
import requests
import json
import urllib3
import subprocess

ssc_path = "/usr/local/bin/exiftool"


def main():
    load_metadata_lookup('/Users/rbruins/Downloads/homebox/Raw/VerfSprayDiYBox')
    #compare_files()


def load_metadata_lookup(locDir):
    for dirname, dirnames, filenames in os.walk(locDir):
        for filename in filenames:
            FileLoc=(dirname + '/' + filename)
            #print(FileLoc)
            if "box1_22" in FileLoc:
                exif_json = call_ssc(FileLoc)
                #print(exif_json)
                for item in exif_json:
                    taglist = item['XMP:TagsList']
                    for tag in taglist:
                        print(tag)


def call_ssc(FileLoc):
    cmd = "-j -G -n"
    ssc_exec = f"{ssc_path} {cmd} '{FileLoc}'"
    output = str(subprocess.check_output(f"{ssc_exec}", shell=True, encoding='utf-8',stderr=subprocess.DEVNULL))
    output = os.linesep.join([s for s in output.splitlines() if s])
    #print(output)
    return json.loads(output)


if __name__ == '__main__':
    main()

