from serpy.fields import (
    Field, MethodField, BoolField, IntField, FloatField, StrField, DatetimeField)

from obj import Obj

import unittest

class TestFields(unittest.TestCase):

    def test_to_value_noop(self):
        self.assertEqual(Field().to_value(5), 5)
        self.assertEqual(Field().to_value('a'), 'a')
        self.assertEqual(Field().to_value(None), None)

    def test_as_getter_none(self):
        self.assertEqual(Field().as_getter(None, None), None)

    def test_is_to_value_overridden(self):
        class TransField(Field):
            def to_value(self, value):
                return value

        field = Field()
        self.assertFalse(field._is_to_value_overridden())
        field = TransField()
        self.assertTrue(field._is_to_value_overridden())
        field = IntField()
        self.assertTrue(field._is_to_value_overridden())

    def test_str_field(self):
        field = StrField()
        self.assertEqual(field.to_value('a'), 'a')
        self.assertEqual(field.to_value(5), '5')

    def test_bool_field(self):
        field = BoolField()
        self.assertTrue(field.to_value(True))
        self.assertFalse(field.to_value(False))
        self.assertTrue(field.to_value(1))
        self.assertFalse(field.to_value(0))

    def test_int_field(self):
        field = IntField()
        self.assertEqual(field.to_value(5), 5)
        self.assertEqual(field.to_value(5.4), 5)
        self.assertEqual(field.to_value('5'), 5)

    def test_float_field(self):
        field = FloatField()
        self.assertEqual(field.to_value(5.2), 5.2)
        self.assertEqual(field.to_value('5.5'), 5.5)

    def test_method_field(self):
        class FakeSerializer(object):
            def get_a(self, obj):
                return obj.a

            def z_sub_1(self, obj):
                return obj.z - 1

        serializer = FakeSerializer()

        fn = MethodField().as_getter('a', serializer)
        self.assertEqual(fn(Obj(a=3)), 3)

        fn = MethodField('z_sub_1').as_getter('a', serializer)
        self.assertEqual(fn(Obj(z=3)), 2)

        self.assertTrue(MethodField.getter_takes_serializer)

    def test_field_label(self):
        field1 = StrField(label="@id")
        self.assertEqual(field1.label, "@id")

    
    def test_datetime_field(self):
        # Test with no format specified
        datetime_str = "2022-01-01T12:00:00Z"
        expected_isoformat = '2022-01-01T12:00:00+00:00'
        result = DatetimeField().to_value(datetime_str)
        self.assertEqual(result, expected_isoformat)

        # Test with custom format
        expected_custom_format = '01/01/2022 12:00 PM'
        custom_format = "%m/%d/%Y %I:%M %p"
        result = DatetimeField(format=custom_format).to_value(datetime_str)
        self.assertEqual(result, expected_custom_format)

        # Test with invalid value
        datetime_str = "invalid datetime"
        result = DatetimeField().to_value(datetime_str)
        self.assertEqual(result, 'invalid datetime')

        # Test with None
        datetime_str = None
        result = DatetimeField().to_value(datetime_str)
        self.assertIsNone(result)



if __name__ == '__main__':
    unittest.main()
