from unittest import TestCase
import Main

class Test(TestCase):
    def test_main(self):
        inputs = ["nobita where am i", "nobita what is the time"]
        for input in inputs:
            assert Main.main(input)

