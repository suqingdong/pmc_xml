import re


def parse_body(body):
    if body is None:
        return []

    def get_data():
        for sec in body.iterfind('sec'):
            title = sec.find('title').text
            sec = sec.find('sec') if sec.find('sec') is not None else sec
            text = '\n\n'.join(''.join(p.itertext()) for p in sec.findall('p'))
            # remove unicode whitespace except \n
            text = re.sub(r'[^\S\n]+', ' ', text).strip()
            yield {'title': title, 'text': text}
    body = list(get_data())
    return body