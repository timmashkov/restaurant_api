from settings.base_exception import BaseAPIException


class MenuAlreadyExists(BaseAPIException):
    status_code = 400
    message = 'Такое меню уже есть'


class MenuNotFound(BaseAPIException):
    status_code = 404
    message = 'menu not found'


class SubMenuAlreadyExists(BaseAPIException):
    status_code = 400
    message = 'Такое подменю уже есть'


class SubMenuNotFound(BaseAPIException):
    status_code = 404
    message = 'submenu not found'


class DishAlreadyExists(BaseAPIException):
    status_code = 400
    message = 'Такое блюдо уже есть'


class DishNotFound(BaseAPIException):
    status_code = 404
    message = 'dish not found'
