from eth_utils import keccak
import hexbytes

def hex_to_dec(hex_string):
    if hex_string is None:
        return None
    try:
        return int(hex_string, 16)
    except ValueError:
        print("Not a hex string %s" % hex_string)
        return hex_string


def to_int_or_none(val):
    if isinstance(val, int):
        return val
    if val is None or val == '':
        return None
    try:
        return int(val)
    except ValueError:
        return None


def chunk_string(string, length):
    return (string[0 + i:length + i] for i in range(0, len(string), length))


def to_normalized_address(address):
    if address is None or not isinstance(address, str):
        return address
    return address.lower()


def validate_range(range_start_incl, range_end_incl):
    if range_start_incl < 0 or range_end_incl < 0:
        raise ValueError('range_start and range_end must be greater or equal to 0')

    if range_end_incl < range_start_incl:
        raise ValueError('range_end must be greater or equal to range_start')

# remove redundancy in topic
def split_to_words(data):
    if type(data) is hexbytes.main.HexBytes:
        data = data.hex()
    if data and len(data) > 2:
        data_without_0x = data[2:]
        words = list(chunk_string(data_without_0x, 64))
        words_with_0x = list(map(lambda word: '0x' + word, words))
        return words_with_0x
    return []


# convert topic to address
def word_to_address(param):
    if param is None:
        return None
    elif len(param) >= 40:
        return to_normalized_address('0x' + param[-40:])
    else:
        return to_normalized_address(param)


# hash abi to be topic
def get_topic_filter(event_abi):
    input_string = event_abi.get("name") + "("
    for input in event_abi.get("inputs"):
        input_string += input.get("type") + ","
    input_string = input_string[:-1] + ")"
    hash = keccak(text=input_string)
    return '0x' + hash.hex()


# get params from abi
def get_list_params_in_order(event_abi):
    indexed = []
    non_indexed = []
    for input in event_abi.get('inputs'):
        if input.get('indexed'):
            indexed.append(input)
        else:
            non_indexed.append(input)
    return indexed + non_indexed


def get_all_address_name_field(event_abi):
    address_name_field = []
    for input in event_abi.get('inputs'):
        if input.get('type') == 'address':
            address_name_field.append(input.get('name'))
    return address_name_field


def convert_even_type(event_type):
    event_type = event_type.upper()
    if event_type == 'LIQUIDATIONCALL':
        return 'LIQUIDATE'
    return event_type