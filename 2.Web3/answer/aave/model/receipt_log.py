class EthEvent(object):
    def __init__(self):
        self.contract_address = None
        self.transaction_hash = None
        self.log_index = None
        self.block_number = None
        self.params = {}
        self.event_type = None

class EventSubscriber:
    def __init__(self, topic_hash, name, list_params_in_order):
        self.topic_hash = topic_hash
        self.name = name
        self.list_params_in_order = list_params_in_order

class EthReceiptLog(object):
    def __init__(self):
        self.log_index = None
        self.transaction_hash = None
        self.transaction_index = None
        self.block_hash = None
        self.block_number = None
        self.address = None
        self.data = None
        self.topics = []