import logging

def init_logging(module_symbol):
    logging.basicConfig(format='%(asctime)s %(message)s',
                        filename='logs/%s.log'%module_symbol,level=logging.INFO)
