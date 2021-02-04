import re
import gzip


def is_comment(line: str) -> bool:
    line = line.strip()
    return True if line[:1] == '#' else False


def file_reader(path: str) -> str:
    with open(path) as file_handler:
        for line in file_handler:
            if not is_comment(line):
                yield line


def gzip_file_reader(path: str) -> str:
    with gzip.open(path, 'rt') as file_handler:
        for line in file_handler:
            if not is_comment(line):
                yield line


def check_no_key(line: str) -> bool:
    line = re.sub('[<].*[:].*[>]', '<URL>', line)
    return True if (line.find(':') == -1) or (line.find(':') == len(line) - 1) else False


def add_line(base_value: str, added_value: str) -> str:
    return '{}\n{}'.format(base_value, added_value)


def parse_document(document: list) -> dict:
    """Parse list of string to dictionary"""
    result: dict[str, str] = {}
    for line in document:
        if check_no_key(line):
            result[last_key] = add_line(result.pop(last_key), line)
        else:
            key, value = line.split(':', 1)
            if key in result:
                result[key] = add_line(result.pop(key), value.strip())
            else:
                result[key.strip()] = value.strip()
            last_key = key
    return result


def get_document(file) -> list:
    document: list = []
    for line in file:
        line = line.strip()
        if line == '':
            if len(document) > 0:
                yield document
            document: list = []
        else:
            document.append(line)


def parse_file(path: str) -> dict:
    if re.match('.*\.gz', path) is not None:
        file = gzip_file_reader(path)
    else:
        file = file_reader(path)
    for document in get_document(file):
        yield parse_document(document)


def load_data(path: str) -> None:
    parsed_data = parse_file(path)

    for document in parsed_data:
        print(document)


if __name__ == '__main__':
    load_data('example.txt.gz')
