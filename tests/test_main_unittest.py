import unittest
from unittest.mock import patch

import main
from main import check_document_existance, \
    get_doc_owner_name, \
    get_all_doc_owners_names, \
    remove_doc_from_shelf, \
    add_new_shelf, \
    append_doc_to_shelf, \
    delete_doc, \
    get_doc_shelf, \
    move_doc_to_shelf, \
    show_document_info, \
    show_all_docs_info, \
    add_new_doc


class Test(unittest.TestCase):
    def setUp(self):
        main.documents = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
        ]

        main.directories = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

    def test_check_document_existence_True(self):
        actual = check_document_existance('10006')

        self.assertTrue(actual)

    def test_check_document_existence_False(self):
        actual = check_document_existance('10008')

        self.assertFalse(actual)

    @patch('builtins.input', lambda *args: '10006')
    def test_get_doc_owner_name(self):
        actual = get_doc_owner_name()
        expected = "Аристарх Павлов"

        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: '10008')
    def test_get_doc_owner_name_doc_number_not_exist(self):
        actual = get_doc_owner_name()
        expected = None

        self.assertEqual(expected, actual)

    def test_get_all_doc_owners_names(self):
        actual = get_all_doc_owners_names()
        expected = {'Василий Гупкин', 'Аристарх Павлов', 'Геннадий Покемонов'}

        self.assertEqual(expected, actual)

    def test_remove_doc_from_shelf_true(self):
        actual = remove_doc_from_shelf('10006')
        expected = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': [],
            '3': []
        }

        self.assertEqual(expected, actual)

    def test_remove_doc_from_shelf_false(self):
        actual = remove_doc_from_shelf('10008')

        self.assertFalse(actual)

    def test_add_new_shelf(self):
        actual = add_new_shelf('4')
        expected = ('4', True)

        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: '5')
    def test_add_new_shelf_with_input(self):
        actual = add_new_shelf()
        expected = ('5', True)

        self.assertEqual(expected, actual)

    def test_add_not_new_shelf(self):
        actual = add_new_shelf('3')
        expected = ('3', False)

        self.assertEqual(expected, actual)

    def test_append_doc_to_shelf(self):
        actual = append_doc_to_shelf('10008', '3')
        expected = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': ['10008']
        }

        self.assertEqual(expected, actual)

    def test_append_doc_to_new_shelf(self):
        actual = append_doc_to_shelf('10008', '4')
        expected = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': [],
            '4': ['10008']
        }

        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: '10006')
    def test_delete_doc(self):
        actual = delete_doc()
        actual_dir = main.directories
        expected = ('10006', True)
        expected_dir = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': [],
            '3': []
        }

        self.assertEqual(expected, actual)
        self.assertEqual(expected_dir, actual_dir)

    @patch('builtins.input', lambda *args: '10008')
    def test_delete_doc_not_exist_doc(self):
        actual = delete_doc()
        actual_dir = main.directories
        expected = None
        expected_dir = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

        self.assertEqual(expected, actual)
        self.assertEqual(expected_dir, actual_dir)

    @patch('builtins.input', lambda *args: '10006')
    def test_get_doc_shelf_with_exist_doc(self):
        actual = get_doc_shelf()
        expected = '2'

        self.assertEqual(expected, actual)

    @patch('builtins.input', lambda *args: '10008')
    def test_get_doc_shelf_with_exist_shelf(self):
        actual = get_doc_shelf()
        expected = None

        self.assertEqual(expected, actual)

    @patch('builtins.input', side_effect=['10006', '3'])
    def test_move_doc_to_shelf(self, mock_input):
        actual = move_doc_to_shelf()
        expected = 'Документ номер "10006" был перемещен на полку номер "3"'
        actual_dir = main.directories
        expected_dir = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': [],
            '3': ['10006']
        }

        self.assertEqual(expected, actual)
        self.assertEqual(expected_dir, actual_dir)

    @patch('builtins.input', side_effect=['10006', '4'])
    def test_move_doc_to_shelf_with_new_shelf(self, mock_input):
        actual = move_doc_to_shelf()
        expected = 'Документ номер "10006" был перемещен на полку номер "4"'
        actual_dir = main.directories
        expected_dir = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': [],
            '3': [],
            '4': ['10006']
        }
        self.assertEqual(expected, actual)
        self.assertEqual(expected_dir, actual_dir)

    @patch('builtins.input', side_effect=['10008', '3'])
    def test_move_doc_to_shelf_not_exist_doc(self, mock_input):
        actual = move_doc_to_shelf()
        expected = False
        actual_dir = main.directories
        expected_dir = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': []
        }

        self.assertEqual(expected, actual)
        self.assertEqual(expected_dir, actual_dir)

    def test_show_document_info(self):
        test_document = {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"}
        actual = show_document_info(test_document)
        expected = 'passport "2207 876234" "Василий Гупкин"'

        self.assertEqual(expected, actual)

    def test_show_all_docs_info(self):
        actual = show_all_docs_info()
        expected = ('Список всех документов:\n',
                    ['passport "2207 876234" "Василий Гупкин"',
                     'invoice "11-2" "Геннадий Покемонов"',
                     'insurance "10006" "Аристарх Павлов"'])

        self.assertEqual(expected, actual)

    @patch('builtins.input', side_effect=['5555 777777', 'passport', 'Иван Иванов', '3'])
    def test_add_new_doc(self, mock_input):
        actual = add_new_doc()
        actual_dir = main.directories
        actual_doc = main.documents
        expected = '3'
        expected_dir = {
            '1': ['2207 876234', '11-2', '5455 028765'],
            '2': ['10006'],
            '3': ['5555 777777']
        }
        expected_doc = [
            {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
            {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
            {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
            {"type": "passport", "number": "5555 777777", "name": "Иван Иванов"},
        ]

        self.assertEqual(expected, actual)
        self.assertEqual(expected_dir, actual_dir)
        self.assertEqual(expected_doc, actual_doc)
