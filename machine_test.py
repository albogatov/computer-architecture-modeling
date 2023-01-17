"""Tests for machine"""
import unittest
import machine


class MachineTest(unittest.TestCase):
    """Machine tests"""

    def test_hello(self):
        output = machine.main(["code/hello_code.txt", "io/hello_input.txt"])
        self.assertEqual(output, "Hello, world!")

    def test_cat(self):
        output = machine.main(["code/cat_code.txt", "io/cat_input.txt"])
        with open("io/cat_input.txt", "rt", encoding="utf8") as f:
            sample_output = f.read()
            self.assertEqual(output, sample_output)

    def test_prob2(self):
        output = machine.main(["code/prob2_code.txt", "io/prob2_input.txt"])
        b = 1
        c = 2
        sum = 0
        while c < 4000000:
            sum += c
            d = b + (c << 0x01)
            c = d + b + c
            b = d
        sample_output = str(sum)
        self.assertEqual(output, sample_output)
