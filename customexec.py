import traceback
import sys
class dest(Exception):
    """ my custom exception class """
    def __init__(self,f):
        self.msg = f
    def __str__(self):
        _, _, exception = sys.exc_info()
        self.msg = 'HI this is error msg %s %s' % (exception.tb_lineno ,exception.tb_frame.f_code.co_filename)
        return self.msg

try:
    raise dest(43)
except dest:
    print(dest(32))


class CustomException(Exception):
    """ my custom exception class """


try:
    raise CustomException('This is my custom exception')
except CustomException as ex:
    print(ex)