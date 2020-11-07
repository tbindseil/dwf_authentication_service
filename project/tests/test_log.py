import unittest
from unittest.mock import patch, MagicMock
from project.server import log
#import project.server.log

class TestStringMethods(unittest.TestCase):

    @patch('logging.getLogger')
    def test_get_log(self, mock_getLogger):
        mock_log = MagicMock()
        mock_getLogger.return_value = mock_log

        outcome = log.get_log()

        assert(mock_log is outcome)
