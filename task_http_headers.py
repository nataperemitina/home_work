import json

def http_headers_to_json(http_header_path, json_path):
    data = {}
    with open(http_header_path) as f:
        tokens = f.readline().strip().split(' ')
        if tokens[0].startswith('HTTP/'):
            if len(tokens) > 1:
                data['protocol'] = tokens[0]
                data['status_code'] = tokens[1]
            if len(tokens) > 2:
                data['status_message'] = ' '.join(tokens[2::])
        else:
            data['method'] = tokens[0]
            data['uri'] = tokens[1]
            data['protocol'] = tokens[2]
                
        for line in f:
            tupled = line.partition(':')
            if tupled[1]:
                data[tupled[0]] = tupled[2].strip()

    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

