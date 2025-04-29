from django.test import TestCase
from jv_parser.services.json_parser import parse
import os
import json
from pathlib import Path

# Create your tests here.
class JsonParserTestCase(TestCase):

    #def test_output(self):
        #print("This is the output: ", parse('{"name": "John", "sex": "male", "boolean": true, "null": null, "age": 30, "height": 1.75, "array": [1, 2, 3], "object": {"key": "value"}}'))

    def test_empty_input(self):
        with self.assertRaises(Exception) as context:
            parse("")
        self.assertEqual(str(context.exception), "Invalid JSON: Input is empty or contains only whitespace.")

    def test_only_string_input(self):
        with self.assertRaises(Exception) as context:
            parse("string")
        self.assertTrue("Invalid JSON: JSON must start with an object or array." in str(context.exception))

    def test_whitespace_only_input(self):
        with self.assertRaises(Exception) as context:
            parse("   ")
        self.assertTrue("Invalid JSON: Input is empty or contains only whitespace." in str(context.exception))

    def test_nested_objects(self):
        json_string = '{"a": {"b": {"c": {"d": {"e": "value"}}}}}'
        self.assertEqual(parse(json_string), {"a": {"b": {"c": {"d": {"e": "value"}}}}})

    def test_nested_arrays(self):
        json_string = '[1, [2, [3, [4, [5]]]]]'
        self.assertEqual(parse(json_string), [1, [2, [3, [4, [5]]]]])

    def test_mixed_nested_structures(self):
        json_string = '{"a": [1, {"b": [2, {"c": 3}]}]}'
        self.assertEqual(parse(json_string), {"a": [1, {"b": [2, {"c": 3}]}]})

    def test_missing_comma(self):
        json_string = '{"key1": "value1" "key2": "value2"}'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Invalid JSON: Expected ',' or '}', but found something else. at line 1 and index 4, token type: string." in str(context.exception))

    def test_extra_characters(self):
        json_string = '{"object": "value"} "extra value"'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Invalid JSON: Extra value after close at line 1, token type: string." in str(context.exception))

    def test_numbers_for_leading_zeros(self):
        json_string = '{"Numbers cannot have leading zeroes": 013}'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Invalid JSON: Leading zeros in number at line 1." in str(context.exception))

    def test_illegal_backslash(self):
        json_string = r'["Illegal backslash escape: \x15"]'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Invalid JSON: Illegal backslash escape x at line 1." in str(context.exception))

    def test_deeply_nested_arrays(self):
        json_string = '[[[[[[[[[[[[[[[[[[[["Too deep"]]]]]]]]]]]]]]]]]]]]'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Maximum depth exceeded. Maximum depth is 20. Current depth is at 20 at line 1 and index 19, token type: lbracket" in str(context.exception))
    
    def test_deeply_nested_objects(self):
        json_string = '{"a":' * 21 + 'null' + '}' * 21
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Maximum depth exceeded" in str(context.exception))
    
    def test_deeply_nested_combination(self):
        json_string = '{"a": [' * 10 + '{"b": [' * 10 + '"value"' + ']}' * 10 + ']' * 10
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Maximum depth exceeded" in str(context.exception))

    def test_tab_character_in_string(self):
        json_string = r'["	tab	character	in	string	"]'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Invalid JSON: Control character '\\t' at line 1." in str(context.exception))

    def test_exponential_notation(self):
        json_string = '[1.0e+10, 1e00, 2e+00, 2e-00]'
        self.assertEqual(parse(json_string), [1.0e+10, 1e00, 2e+00, 2e-00])

    def test_large_flat_array(self):
        large_json = '[' + ', '.join(str(i) for i in range(100000)) + ']'
        expected = list(range(100000))
        self.assertEqual(parse(large_json), expected)

    def test_large_flat_object(self):
        large_json = '{' + ', '.join(f'"key{i}": {i}' for i in range(100000)) + '}'
        expected = {f"key{i}": i for i in range(100000)}
        self.assertEqual(parse(large_json), expected)

    def test_control_character_in_string(self):
        json_string = '["This is a test\u0001string"]'
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Invalid JSON: Control character '\\x01' at line 1." in str(context.exception))

    # Test cases for Coding challenges test json
    def read_file(self, file):
        with open(file, "r") as f:
            return f.read()
        
    def test_json_parser_step1_invalid(self):
        file = "jv_parser/tests/step1/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertEqual(str(context.exception), "Invalid JSON: Input is empty or contains only whitespace.")

    def test_json_parser_step1_valid(self):
        file = "jv_parser/tests/step1/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {})

    def test_json_parser_step2_invalid(self):
        file = "jv_parser/tests/step2/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
            print("This is the output: ", parse(json_string))
        self.assertTrue("Invalid JSON: Unexpected trailing comma" in str(context.exception))

    def test_json_parser_step2_valid(self):
        file = "jv_parser/tests/step2/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {"key": "value"})
    
    def test_json_parser_step2_invalid2(self):
        file = "jv_parser/tests/step2/invalid2.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Unexpected keyword: key2 at line 3." in str(context.exception))

    def test_json_parser_step2_valid2(self):
        file = "jv_parser/tests/step2/valid2.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {"key": "value", "key2": "value"})

    def test_json_parser_step3_invalid(self):
        file = "jv_parser/tests/step3/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Unexpected keyword: False at line 3. Keywords must be 'true', 'false', or 'null'" in str(context.exception))

    def test_json_parser_step3_valid(self):
        file = "jv_parser/tests/step3/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), { 
                                            "key1": True,
                                            "key2": False,
                                            "key3": None,
                                            "key4": "value",
                                            "key5": 101
                                            })
        
    def test_json_parser_step4_invalid(self):
        file = "jv_parser/tests/step4/invalid.json"
        json_string = self.read_file(file)
        with self.assertRaises(Exception) as context:
            parse(json_string)
        self.assertTrue("Unexpected character: ' at line 7." in str(context.exception))

    def test_json_parser_step4_valid(self):
        file = "jv_parser/tests/step4/valid.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {
                                            "key": "value",
                                            "key-n": 101,
                                            "key-o": {},
                                            "key-l": []
                                            })

    def test_json_parser_step4_valid2(self):
        file = "jv_parser/tests/step4/valid2.json"
        json_string = self.read_file(file)
        self.assertEqual(parse(json_string), {
                                            "key": "value",
                                            "key-n": 101,
                                            "key-o": {
                                                "inner key": "inner value"
                                            },
                                            "key-l": ["list value"]
                                            })

    #json.org test cases
    def test_json_parser_json_org_test_cases(self):
        TEST_DIR = Path("jv_parser/tests/json.org_tests/test").resolve()
        print(f"Test directory: {TEST_DIR}")

        for filename in os.listdir(TEST_DIR):
            if filename.endswith(".json"):
                file_path = TEST_DIR / filename
                with open(file_path, 'r', encoding="utf-8") as file:
                    json_string = file.read()

                print(f"Testing {filename}...")
                    
                if "fail" in filename:
                    with self.assertRaises(Exception):
                        parse(json_string)
                else:
                    expected = json.loads(json_string)
                    result = parse(json_string)
                    self.assertEqual(result, expected)
                   

 