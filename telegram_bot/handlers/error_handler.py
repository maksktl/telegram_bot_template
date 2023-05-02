import logging

from aiogram import Dispatcher

from telegram_bot.handlers.base import BaseHandler


class ErrorHandler(BaseHandler):

    def __init__(self, dp: Dispatcher):
        super().__init__(dp)

    def register_methods(self):
        self.dp.register_errors_handler(ErrorHandler.errors_handler)

    @staticmethod
    async def errors_handler(update, exception):
        """
        Exceptions handler. Catches all exceptions within task factory tasks.
        :param dispatcher:
        :param update:
        :param exception:
        :return: stdout logging
        """
        from aiogram.utils.exceptions import (Unauthorized, InvalidQueryID, TelegramAPIError,
                                              CantDemoteChatCreator, MessageNotModified, MessageToDeleteNotFound,
                                              MessageTextIsEmpty, RetryAfter,
                                              CantParseEntities, MessageCantBeDeleted)

        if isinstance(exception, CantDemoteChatCreator):
            logging.debug("Can't demote chat creator")
            return True

        if isinstance(exception, MessageNotModified):
            logging.debug('Message is not modified')
            return True
        if isinstance(exception, MessageCantBeDeleted):
            logging.debug('Message cant be deleted')
            return True

        if isinstance(exception, MessageToDeleteNotFound):
            logging.debug('Message to delete not found')
            return True

        if isinstance(exception, MessageTextIsEmpty):
            logging.debug('MessageTextIsEmpty')
            return True

        if isinstance(exception, Unauthorized):
            logging.info(f'Unauthorized: {exception}')
            return True

        if isinstance(exception, InvalidQueryID):
            logging.exception(f'InvalidQueryID: {exception} \nUpdate: {update}')
            return True

        if isinstance(exception, TelegramAPIError):
            logging.exception(f'TelegramAPIError: {exception} \nUpdate: {update}')
            return True
        if isinstance(exception, RetryAfter):
            logging.exception(f'RetryAfter: {exception} \nUpdate: {update}')
            return True
        if isinstance(exception, CantParseEntities):
            logging.exception(f'CantParseEntities: {exception} \nUpdate: {update}')
            return True
        logging.exception(f'Update: {update} \n{exception}')
