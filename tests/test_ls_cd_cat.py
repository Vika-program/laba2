import pytest
import tempfile
import os
import shutil
from pathlib import Path
from typer.testing import CliRunner
from src.main import app

@pytest.fixture
def sandbox_dir():
    tempdir = tempfile.mkdtemp()
    yield Path(tempdir)
    shutil.rmtree(tempdir)

class TestLsCdCat:
    @pytest.fixture(autouse=True)
    def preparing(self, sandbox_dir):
        self.sandbox = sandbox_dir
        self.runner = CliRunner()

    def test_ls(self):
        (self.sandbox / "1.txt").write_text('')
        (self.sandbox / "2.txt").write_text('')
        result = self.runner.invoke(app, ['ls', str(self.sandbox)])
        assert result.exit_code == 0
        assert "1.txt" in result.output
        assert "2.txt" in result.output

        new_dir = self.sandbox / "new_dir"
        new_dir.mkdir()
        result2 = self.runner.invoke(app, ['ls', str(new_dir)])
        assert result2.exit_code == 0
        assert "" in result2.output

        result3 = self.runner.invoke(app, ['ls', '2.txt'])
        assert "ls : ошибка" in result3.output

        result4 = self.runner.invoke(app, ['ls', 'not_exist.txt'])
        assert "ls : ошибка" in result4.output

    def test_ls_l(self):
        (self.sandbox / "1.txt").write_text('')
        new_dir = self.sandbox / "new_dir"
        new_dir.mkdir()
        result = self.runner.invoke(app, ['ls', "-l", str(self.sandbox)])
        assert result.exit_code == 0
        for line in result.output.splitlines():
            assert len(line.split()) == 5
        assert "1.txt" in result.output
        assert "new_dir" in result.output

    def test_cd(self):
        path = self.sandbox / "1 level" / "2 level" / "3 level" / "test.txt"
        path.parent.mkdir(parents=True)
        result = self.runner.invoke(app, ['cd', str(path.parent)])
        assert result.exit_code == 0
        assert Path(path.parent).samefile(Path(os.getcwd()))
        #переход в родительскую директорию
        start = os.getcwd()
        result = self.runner.invoke(app, ['cd', ".."])
        assert result.exit_code == 0
        assert Path(os.getcwd()).samefile(Path(start).parent)
        #переход в домашнюю директорию
        result = self.runner.invoke(app, ['cd', "~"])
        assert Path(os.getcwd()).samefile(Path.home())
        assert result.exit_code == 0
        #несуществующий каталог
        result = self.runner.invoke(app, ['cd', "not_exist.txt"])
        assert result.exit_code == 0
        assert "cd: ошибка" in result.output
        #файл вместо каталога
        result = self.runner.invoke(app, ['cd', str(self.sandbox / "1 level" / "2 level" / "3 level" / "test.txt")])
        assert result.exit_code == 0
        assert "cd: ошибка" in result.output
        #точка
        start = Path(os.getcwd())
        result1 = self.runner.invoke(app, ['cd', "."])
        end1 = Path(os.getcwd())
        result2 = self.runner.invoke(app, ['cd'])
        end2 = Path(os.getcwd())
        assert result1.exit_code == 0
        assert result2.exit_code == 0
        assert end1.samefile(end2) and end2.samefile(Path(start))
        #относительный путь
        new_dir = self.sandbox / "new_dir" / "dir2"
        new_dir.mkdir(parents=True)
        os.chdir(self.sandbox)
        result = self.runner.invoke(app, ['cd', "new_dir/dir2"])
        assert result.exit_code == 0
        assert Path(new_dir).samefile(Path(os.getcwd()))

    def test_cat(self):
        #вывести строку
        (self.sandbox / "1.txt").write_text('Hello, world!')
        result = self.runner.invoke(app, ['cat', str(self.sandbox / '1.txt')])
        assert result.exit_code == 0
        assert "Hello, world!" in result.output
        #вывести несколько строк
        (self.sandbox / "2.txt").write_text('Hello, world!\n Hello, world!')
        result = self.runner.invoke(app, ['cat', str(self.sandbox / '2.txt')])
        assert 'Hello, world!\n Hello, world!' in result.output
        #нет разрешения
        os.chmod(str(self.sandbox / '2.txt'), 0o000)
        result = self.runner.invoke(app, ['cat', str(self.sandbox / "2.txt")])
        assert result.exit_code == 0
        assert "Permission denied" in result.output
        #нет файла
        result = self.runner.invoke(app, ['cat', str(self.sandbox / "not_exist.txt")])
        assert "cat : ошибка" in result.output
        #каталог
        result = self.runner.invoke(app, ['cat', str(self.sandbox)])
        assert "cat : ошибка" in result.output
