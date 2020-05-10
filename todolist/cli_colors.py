class cli_colors:
    END = '\u001b[0m'
    RED = '\u001b[31m'
    GREEN = '\u001b[32m'
    BLUE = '\u001b[34m'

def returnError(message):
    print(f"""
{cli_colors.RED} {message} {cli_colors.END}
           """)
