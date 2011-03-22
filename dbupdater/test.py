import unittest

import updater

class UpdaterTests (unittest.TestCase):
    def test_validDateAsExpected(self):
        import datetime as dt
        
        valid = dt.datetime(year=2011, month=3, day=19, hour=1, minute=24, second=0)
        try:
            updater.validate_dt_value(valid)
        except ValueError, e:
            self.fail('Datetime %s should not raise ValueError: %s' % (valid, e))
    
    def test_datetimeWithMicrosecondIsInvalid(self):
        import datetime as dt
        
        invalid = dt.datetime(year=2011, month=3, day=19, hour=1, minute=24, second=0, microsecond=1)
        try:
            updater.validate_dt_value(invalid)
        except ValueError, e:
            pass
        else:
            self.fail('Datetime %s should raise ValueError' % (invalid))
        
    def test_datetimeWithTimezoneIsInvalid(self):
        import datetime as dt
        
        ZERO = dt.timedelta(0)
        HOUR = dt.timedelta(hours=1)

        # A UTC class.

        class UTC(dt.tzinfo):
            """UTC"""

            def utcoffset(self, dt):
                return ZERO

            def tzname(self, dt):
                return "UTC"

            def dst(self, dt):
                return ZERO

        utc = UTC()

        invalid = dt.datetime(year=2011, month=3, day=19, hour=1, minute=24, second=0, tzinfo=utc)
        try:
            updater.validate_dt_value(invalid)
        except ValueError, e:
            pass
        else:
            self.fail('Datetime %s should raise ValueError' % (invalid))
    
    def test_recordsParsedAsExpected(self):
        from StringIO import StringIO
        
        stream = StringIO("""<?xml version="1.0" encoding="utf-8"?>

            <service_requests>
                <request>
                    <name>Bob</name>
                    <age>23</age>
                </request>
                
                <request>
                    <name>Jill</name>
                    <age></age>
                </request>
            </service_requests>
        """)
        
        requests = updater.parse_requests_doc(stream)
        self.assertEqual(requests, [{'name':'Bob','age':'23'},{'name':'Jill'}])

if __name__ == '__main__':
    unittest.main()
