import re
from django.core.exceptions import ValidationError

def validate_cron_string(cron_string):
    print("in validator...")
    pattern = r'^(\*|\d+|\d+(?:-\d+)?|\*(?:\/\d+)?|\d+(?:-\d+)?(?:\/\d+)?) (\*|\d+|\d+(?:-\d+)?|\*(?:\/\d+)?|\d+(?:-\d+)?(?:\/\d+)?) (\*|\d+|\d+(?:-\d+)?|\*(?:\/\d+)?|\d+(?:-\d+)?(?:\/\d+)?) (\*|\d+|\d+(?:-\d+)?|\*(?:\/\d+)?|\d+(?:-\d+)?(?:\/\d+)?) (\*|\d+|\d+(?:-\d+)?|\*(?:\/\d+)?|\d+(?:-\d+)?(?:\/\d+)?)$'
    return bool(re.match(pattern, cron_string))

