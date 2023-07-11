import re
import sys
import os

def main():
    #Preamble; loading files.
    if len(sys.argv) != 3:
        print("Usage: centrifuge_files.py [FILENAME] [DEST FOLDER]")
        exit(1)

    #Check that the input file exists.
    try:
        file = open(sys.argv[1], "r", encoding="utf-8")
    except OSError:
        print(f"Could not open input file: {sys.argv[1]}")
        exit(1)

    #Check that the destination folder exists.
    if not os.path.exists(sys.argv[2]):
        file.close()
        print(f"Destination folder does not exist: {sys.argv[2]}")
        exit(1)

    #Read the file!
    print(f"Reading {sys.argv[1]}...")
    text = file.readlines()
    inferred_video_group = ""
    found_video_numbers = []
    for line in text:
        match = re.search(r".*? [0-9]*?$", line)

        if match:
            print(f"Found {match.group(0)}.")
            if len(match.group(0).split()) < 2:
                print("Malformed line found!")
                print(f"Suspicious line: {match.group(0)}")
                print("Enter to transcribe into output file if Japanese text, CTRL+C to exit.")
                _ = sys.stdin.readline()
                transcribe_line(line, inferred_video_group, found_video_numbers)
                continue
            if inferred_video_group == "":
                inferred_video_group = match.group(0).split()[0]
                print(f"Inferred the inputted video group is {inferred_video_group}, is this correct?")
                print("Enter if yes, CTRL+C if no.")
                _ = sys.stdin.readline()
            if inferred_video_group != match.group(0).split()[0]:
                print(f"Inferred video group ({inferred_video_group}) does not match this found title ({match.group(0).split()[0]}), malformed?")
                print("Enter to transcribe into output file if Japanese text, CTRL+C to exit.")
                _ = sys.stdin.readline()
                transcribe_line(line, inferred_video_group, found_video_numbers)
                continue
            found_video_number = int(match.group(0).split()[1])

            #Not all transcripts start at entry 1, and not all entries follow each other sequentially,
            #so we need to keep track of which video files we have centrifuge-d to check (manually) later.
            found_video_numbers.append(found_video_number)
            #Don't want to include the title, "Cou 001" etc., in the new file, so skip matched lines.
            continue

        transcribe_line(line, inferred_video_group, found_video_numbers)

    found_video_numbers.sort()
    print("Found these video numbers:")
    print(found_video_numbers)
    file.close()

def transcribe_line(line, inferred_video_group, found_video_numbers):
    if len(found_video_numbers) == 0 or inferred_video_group == "":
        print("Tried to transcribe a line with no associated output file to use!")
        print("(Lines before a header, e.g. \"Cou 001\"?)")
        print(f"Suspicious line: {line}")
        print("Enter to ignore, CTRL+C to exit.")
        _ = sys.stdin.readline()
        return

    #Quick fix to make sure video numbers start with leading zeroes.
    title_number = str(found_video_numbers[-1])
    if len(title_number) == 1:
        title_number = '00' + title_number
    if len(title_number) == 2:
        title_number = '0' + title_number
        
    output_filename = inferred_video_group + title_number

    try:
        if sys.argv[2][-1] != '/':
            raise OSError("DEST FOLDER should have a '/' at the end.")
        output_file = open(sys.argv[2] + output_filename, "a")
        output_file.write(line)
    except OSError:
        print(f"Could not write to file: {sys.argv[2] + output_filename}")
        print("DEST FOLDER should have a '/' at the end because I'm lazy.")
        print("Exiting...")
        exit(1)

if __name__ == "__main__":
    main()
