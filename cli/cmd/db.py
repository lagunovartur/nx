import datetime as dt
import os
from argparse import Namespace, ArgumentParser
from config import config
from abstract import Command
from runner import run


@run(from_env='db', execute=True)
def db_shell():
    """psql"""
    return f"sh -c 'export PGPASSWORD=$POSTGRES_PASSWORD && psql -U $POSTGRES_USERNAME -d $POSTGRES_DATABASE'"

@run(from_env='db', execute=True)
def db_dump():
    """pg_dump"""

    dump_dir = config.db_dump_dir
    now = dt.datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
    dump_file = os.path.join(dump_dir, f"{now}.sql")

    return f"""sh -c '
        mkdir -p {dump_dir} && 
        chmod 777 {dump_dir} &&
        export PGPASSWORD=$POSTGRES_PASSWORD &&
        pg_dump -U $POSTGRES_USERNAME -d $POSTGRES_DATABASE > {dump_file} &&
        chmod 777 {dump_file}'  
    """

class DbRestore(Command):
    """db < dump_file"""

    @run(from_env='db', execute=True)
    def __call__(self, args: Namespace):

        try:
            dump = int(args.dump)
        except Exception as e:
            dump = args.dump

        if isinstance(dump, int):
            try:
                dump_file = self._dump_files()[dump]
            except IndexError:
                raise IndexError('Не найден фаил по индексу')
        else:
            dump_file = dump

        dump_file = config.db_dump_dir.joinpath(dump_file)

        return f"""sh -c '
            export PGPASSWORD=$POSTGRES_PASSWORD &&
            psql -U $POSTGRES_USERNAME -c "DROP DATABASE IF EXISTS $POSTGRES_DATABASE" &&
            psql -U $POSTGRES_USERNAME -c "CREATE DATABASE $POSTGRES_DATABASE" &&
            psql -U $POSTGRES_USERNAME -d $POSTGRES_DATABASE < {dump_file}'
        """



    def add_args(self, parser: ArgumentParser) -> None:
        parser.add_argument('dump', help='дамп для восстановления')

    def _dump_files(self):

        @run(from_env='db', capture_output=True, check=False)
        def get_dump_files():
            dump_dir = config.db_dump_dir
            return f"ls {dump_dir} -p  | grep -v / | sort"

        try:
            res = get_dump_files()
        except Exception as e:
            return []

        if not res:
            return []

        return res[0].stdout.strip().split('\n')

db_restore = DbRestore()




