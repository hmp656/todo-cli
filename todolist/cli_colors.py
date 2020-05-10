class cli_colors:
    END = '\e[0m'
    RED = '\e[1;31m'
    GREEN = '\e[1;32m'
    BLUE = '\e[1;34m'

def returnError(message):
    print(f"""
{cli_colors.RED} {message} {cli_colors.END}
           """)
