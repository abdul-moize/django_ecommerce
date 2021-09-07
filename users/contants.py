email_regex = '''
            \\b[a-z0-9]+        # must start with at least one lower case letter or digit
            [a-zA-Z0-9.-_]*     # followed by 0 or more digits, '.', '-', '_' 
            @                   # followed by at the rate sign '@' 
            [a-z]+              # followed by at least one lowercase letter        
            [0-9-_]*            # followed by 0 or more digits, '-', '_'
            \\.com\\b           # Must end with .com
'''
password_regex = '''
'''