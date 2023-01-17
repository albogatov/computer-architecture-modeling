"""Tests for translator"""
import unittest
import isa
import translator


class TranslatorTest(unittest.TestCase):
    """Translator tests"""
    def template_test(self, input_file, output_file, sample_output_file):
        translator.main([input_file, output_file])
        result_code = isa.read_code(output_file)
        correct_code = isa.read_code(sample_output_file)
        self.assertEqual(result_code, correct_code)

    def test_hello(self):
        print("hello")
        self.template_test("asm_src/hello.txt", "code/hello_code.txt", "code/hello_sample_code.txt")

    def test_cat(self):
        print("cat")
        self.template_test("asm_src/cat.txt", "code/cat_code.txt", "code/cat_sample_code.txt")

    def test_prob2(self):
        print("prob2")
        self.template_test("asm_src/prob2.txt", "code/prob2_code.txt", "code/prob2_sample_code.txt")


if __name__ == '__main__':
    unittest.main()
