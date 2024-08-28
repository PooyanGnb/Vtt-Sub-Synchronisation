import csv
import re

def remove_html_tags(text):
    """
    Remove HTML tags from a string using regular expressions.
    Args:
        text (str): The input string containing HTML tags.

    Returns:
        str: The cleaned string with HTML tags removed.
    """
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)

def parse_vtt(file_path):
    """
    Parse a VTT file to extract subtitles and merge entries with the same start time.
    Args:
        file_path (str): Path to the VTT file.

    Returns:
        list: Sorted list of tuples, each containing the start time and merged text.
    """
    subtitle_dict = {}
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        i = 0
        while i < len(lines): # line by line
            line = lines[i].strip()
            if '-->' in line: # the line having timestamps
                time_range = line.split(' --> ')[0] # starting time
                text = []
                i += 1
                while i < len(lines) and lines[i].startswith("<"): # lines having subtitle text
                    if lines[i].strip():
                        clean_text = remove_html_tags(lines[i].strip())
                        if clean_text: 
                            text.append(clean_text if not text else "\n" + clean_text) # add new line if needed
                    i += 1
                if text:
                    merged_text = ' '.join(text)
                    subtitle_dict[time_range] = subtitle_dict.get(time_range, '') + ' ' + merged_text
            else:
                i += 1
    return sorted((k, v) for k, v in subtitle_dict.items())

def align_subtitles(first_subs, second_subs):
    """
    Align subtitles from two different language sources based on timestamps.
    Args:
        first_subs (list): List of tuples from the first subtitle source.
        second_subs (list): List of tuples from the second subtitle source.

    Returns:
        list: List of aligned subtitle entries, each a tuple of three elements.
    """
    aligned_subs = []
    i = 0
    for first_start, first_text in first_subs:
        closest_sub = min(second_subs, key=lambda x: abs(parse_time(x[0]) - parse_time(first_start))) # finding the closest subtitle to the first subtitle
        if i != 0 and closest_sub[0] == aligned_subs[i-1][3]: # if second sub has been appended before
            aligned_subs[i-1][1] += " " + first_text # first sub gets added to appended sub
        elif i != 0 and first_start == aligned_subs[i-1][0]: # if first sub has been appended before
            aligned_subs[i-1][2] += " " + closest_sub[1] # second sub gets added to appended sub
        else: # if non of them were appended before
            aligned_subs.append([first_start, first_text, closest_sub[1], closest_sub[0]])
            i += 1

    # Transform the start time of each entry using the change_time_format function
    for entry in aligned_subs:
        entry[0] = change_time_format(entry[0])

    return [entry[:3] for entry in aligned_subs] # only returning the first 3 elements of each index (removing the second sub timestamp)

def parse_time(t):
    """
    Convert a VTT timestamp into seconds.
    Args:
        t (str): Timestamp string in 'HH:MM:SS,mmm' format.

    Returns:
        float: The time in seconds.
    """
    h, m, s = map(float, t.replace(',', '.').split(':'))
    return h * 3600 + m * 60 + s

def change_time_format(time):
    """
    Convert a standard time format into a simplified and more readable format.
    
    Args:
        time (str): A string representing the time in 'HH:MM:SS,mmm' or 'HH:MM:SS.mmm' format.
    
    Returns:
        str: A simplified time format. Formats are:
            - 'XXs' for times less than a minute.
            - 'MM:SS' for times less than an hour.
            - 'HH:MM:SS' for times that are an hour or longer.
    """

    # Split the time string by ':' and convert each part into seconds.
    # Also handle milliseconds by replacing commas with dots for float conversion.
    h, m, s = map(float, time.replace(',', '.').split(':'))
    
    # Calculate the total seconds from the hours, minutes, and seconds.
    total_seconds = int(h * 3600 + m * 60 + s)
    
    # If the total seconds are less than 60, return the seconds with an 's' suffix.
    if total_seconds < 60:
        return f"{total_seconds}s"
    
    # If the total seconds are less than an hour, return in 'MM:SS' format.
    elif total_seconds < 3600:
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        return f"{minutes}:{seconds:02d}"
    
    # Otherwise, return the time in 'HH:MM:SS' format for durations of an hour or longer.
    else:
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        return f"{hours}:{minutes:02d}:{seconds:02d}"

def export_to_csv(subtitles, filename):
    """
    Export subtitles to a CSV file.
    Args:
        subtitles (list): List of subtitles to write.
        filename (str): Output filename for the CSV.
    """
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Time', 'First', 'Second'])
        for sub in subtitles:
            writer.writerow(sub)