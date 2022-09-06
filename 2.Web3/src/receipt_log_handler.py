import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))
from service.utils import *
import logging
from model.receipt_log import *

logger = logging.getLogger('EthLogService')


class EthReceiptLogHandler(object):

    def build_list_info_event(self, abi):
        list_ = []
        for i in abi:
            arr = self.init_events_subscription(i)
            if not arr:
                continue
            else:
                list_.append(arr)
        return list_

    def init_events_subscription(self, abi):
        event_abi = abi
        if event_abi.get('type') == 'event':
            method_signature_hash = get_topic_filter(event_abi)
            list_params_in_order = get_list_params_in_order(event_abi)
            event_name = event_abi.get('name')
            event_subscriber = EventSubscriber(method_signature_hash, event_name, list_params_in_order)
            topic = method_signature_hash
            address_name_field = get_all_address_name_field(event_abi)
            return [event_subscriber, topic, address_name_field, event_name]
        return []

    def eth_event_to_dict(self, eth_event: EthEvent):
        d1 = {
            'type': 'event',
            'event_type': convert_even_type(eth_event.event_type),
            'contract_address': eth_event.contract_address,
            'transaction_hash': eth_event.transaction_hash,
            'log_index': eth_event.log_index,
            'block_number': eth_event.block_number,
        }
        d2 = eth_event.params
        return {**d1, **d2}

    def web3_dict_to_receipt_log(self, dict):
        receipt_log = EthReceiptLog()

        receipt_log.log_index = dict.get('logIndex')

        transaction_hash = dict.get('transactionHash')
        if transaction_hash is not None:
            transaction_hash = transaction_hash.hex()
        receipt_log.transaction_hash = transaction_hash

        block_hash = dict.get('blockHash')
        if block_hash is not None:
            block_hash = block_hash.hex()
        receipt_log.block_hash = block_hash
        receipt_log.block_number = dict.get('blockNumber')
        receipt_log.address = dict.get('address')
        receipt_log.data = dict.get('data')

        if 'topics' in dict:
            receipt_log.topics = [topic.hex() for topic in dict['topics']]

        return receipt_log

    def decode_data_by_type(self, data, type):
        if self.is_integers(type):
            return hex_to_dec(data)
        elif type == "address":
            return word_to_address(data)
        else:
            return data

    def is_integers(self, type):
        return type == "uint256" or type == "uint128" or type == "uint64" or type == "uint32" or type == "uint16" or type == "uint8" or type == "uint" \
               or type == "int256" or type == "init128" or type == "init64" or type == "init32" or type == "init16" or type == "init8" or type == "init"

    def extract_event_from_log(self, receipt_log, event_subscriber):
        topics = receipt_log.topics
        if topics is None or len(topics) < 1:
            logger.warning("Topics are empty in log {} of transaction {}".format(receipt_log.log_index,
                                                                                 receipt_log.transaction_hash))
            return None
        if event_subscriber.topic_hash == topics[0]:
            # Handle unindexed event fields
            topics_with_data = topics + split_to_words(receipt_log.data)
            list_params_in_order = event_subscriber.list_params_in_order
            # if the number of topics and fields in data part != len(list_params_in_order), then it's a weird event
            num_params = len(list_params_in_order)
            topics_with_data = topics_with_data[1:]
            if len(topics_with_data) != num_params:
                logger.warning("The number of topics and data parts is not equal to {} in log {} of transaction {}"
                               .format(str(num_params), receipt_log.log_index, receipt_log.transaction_hash))
                return None

            event = EthEvent()
            event.contract_address = to_normalized_address(receipt_log.address)
            event.transaction_hash = receipt_log.transaction_hash
            event.log_index = receipt_log.log_index
            event.block_number = receipt_log.block_number
            event.event_type = event_subscriber.name
            for i in range(num_params):
                param_i = list_params_in_order[i]
                name = param_i.get("name")
                type = param_i.get("type")
                data = topics_with_data[i]
                event.params[name] = str(self.decode_data_by_type(data, type))
            return event

        return None

if __name__=="__main__":
    import json
    m = EthReceiptLogHandler()
    with open("../abi/event_abi.json", "r") as f:
        a = json.loads(f.read())
    print(m.build_list_info_event(a))