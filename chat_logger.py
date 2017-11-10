import logging

__author__ = 'avi0gaur'


class BotLogger:

    def __init__(self):
        """
        File path of logger
        """
        f = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        try:
            logging.basicConfig(filename='../logs/chatbot.log', level=logging.DEBUG,format=f)
        except OSError as err:
            print("OS error: {0}".format(err))
        self.log = logging.getLogger("bot_logs")


    def log_debug(self, str):
        """
        Provide logs for debug states, ensure debug level is set.
        :param str:
        :return:
        """
        self.log.debug(str)

    def log_info(self, str):
        """
        Provide logs for Info states, ensure debug level is set.
        :param str:
        :return:
        """
        self.log.info(str)

    def log_warning(self, str):
        """
         Provide logs for Info states, ensure debug level is set.
         :param str:
         :return:
        """
        self.log.warning(str)

    def log_error(self, str):
        """
            Provide logs for Error states, ensure debug level is set.
            :param str:
            :return:
        """
        self.log.error(str)

    def log_critical(self, str):
        """
            Provide logs for critical states, ensure debug level is set.
            :param str:
            :return:
        """
        self.log.critical(str)
