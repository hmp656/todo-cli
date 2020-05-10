from . import checks
from .cli_colors import cli_colors as cli_col
from .cli_colors import returnError
import sqlite3 as sql
from .sqlite_com import databaseBuild, dropTable, databaseCols 
from .sqlite_com import conn_cursor as curse
from .sqlite_com import SQL_EComm as ecom
from .sqlite_com import SQL_RComm as rcom
from .sqlite_com import columns
from collections import namedtuple
import os.path, click


if not os.path.isfile('todolist.db'):
    databaseBuild()
else:
    if not databaseCols(columns):
        dropTable()
        databaseBuild()


Task = namedtuple('Task', columns)



def getItems(command='incomplete'):
    c = curse()
    if command == 'incomplete':
        c[0].execute(rcom.READ_Incomplete)

    if command == 'complete':
        c[0].execute(rcom.READ_Complete)

    if command == 'all':
        c[0].execute(rcom.READ_All)

    return c[0].fetchall()



def searchTags(query):
    c = curse()
    d = curse()
    if query:
        c[0].execute(rcom.READ_TagInComp, (query,))
        d[0].execute(rcom.READ_TagComp, (query,))
        return c[0].fetchall(), d[0].fetchall()
    else:
        return None



def createList(items):
    listed = []
    for item in map(Task._make, items):
        listed.append(item)

    return(listed)



def list_format(items):
    for item, index in zip(items, range(0, len(items))):
        index = str(index + 1) + ') '

        if item[3] == None:
            tags = ' '
        else:
            tags = ' #' + str(item[3])

        if item[2] and checks.checkDateFormat(item[2]):
            daysLeft = checks.dateDif(item[2])
            if daysLeft > 0:
                yield index + item[1] + ' (Due ' + cli_col.BLUE + checks.daysConvert(daysLeft) + cli_col.END + ')' + tags
            elif daysLeft == 0:
                yield index + item[1] + ' (Due ' + cli_col.GREEN + checks.daysConvert(daysLeft) + cli_col.END + ')' + tags
            elif daysLeft < 0:
                yield index + item[1] + ' (Due ' + cli_col.RED + checks.daysConvert(daysLeft) + cli_col.END + ')' + tags

        else:
            yield index + item[1] + tags



def editList(ID_Code, title=None, expiry_date=None, tags=None, status=0, command='add'):
    c = curse()

    if command == 'add' and title:
        c[0].execute(ecom.ADD_Comm, (ID_Code, title, expiry_date, tags, status))

    elif command == 'edit':
        c[0].execute(ecom.EDIT_Comm, (title, expiry_date, ID_Code))

    elif command == 'tag':
        c[0].execute(ecom.TAG_Comm, (tags, ID_Code))

    elif command == 'remove':
        c[0].execute(ecom.REM_Comm, (ID_Code,))

    c[1].commit()
    c[1].close()



@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx=None):
    if not ctx.invoked_subcommand:
        items = getItems('incomplete')
        for item in list_format(createList(items)):
            print(item)

# view all tasks
@main.command()
@click.option('--command', default='incomplete', nargs=1)
def view(command):
    items = getItems(command)
    for item in list_format(createList(items)):
        print(item)


# search tags
@main.command()
def search():
    tag_search = input('Enter tag: ')
    results = searchTags(tag_search)
    count = 0

    for result in results:
        count += 1
        if not result:
            if count == 1:
                print('No incomplete tasks with this tag.')
                print('\n')

            elif count == 2:
                print('No complete tasks with this tag.')
                # print('\n')

        else:
            if count == 1:
                print('Incomplete tasks:')
                for item in list_format(createList(result)):
                    print(item)
                    print('\n')

            elif count == 2:
                print('Complete tasks:')
                for item in list_format(createList(result)):
                    print(item)
                    # print('\n')


# add a task
@main.command()
def add():
    title_task = input('Enter title: ')
    title_date = input('Enter date (DD/MM/YYYY): ')

    if checks.checkDateFormat(title_date):
        editList(checks.createID(), title=title_task, expiry_date=title_date)
    else:
        editList(checks.createID(), title=title_task)


# edit title and date
@main.command()
@click.argument('index', nargs=1, type=int)
def edit(index):
    title_task = input('Enter title: ')
    title_date = input('Enter date (DD/MM/YYYY): ')

    items = getItems()
    try:
        if checks.checkDateFormat(title_date):
            editList(items[index-1][0], title_task, title_date, command='edit')
        else:
            editList(items[index-1][0], title_task, command='edit')

    except Exception as e:
        returnError(e)


# add a tag
@main.command()
@click.argument('index', nargs=1, type=int)
def tag(index):
    title_tag = input('Enter tag: ')

    items = getItems()
    editList(items[index-1][0], tags=title_tag, command='tag')



# remove
@main.command()
@click.argument('index', nargs=1, type=int)
def rem(index):
    items = getItems()
    try:
        editList(items[index-1][0], command='remove')
    except Exception as e:
        returnError(e)


@main.command()
def rebuildDB():
    dropTable()
    databaseBuild()


if __name__ == '__main__':
    main()
