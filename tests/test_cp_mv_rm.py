import pytest
import tempfile
import shutil
import os
from pathlib import Path
from typer.testing import CliRunner
from src.main import app

@pytest.fixture
def sandbox_dir():
    tempdir = tempfile.mkdtemp()
    yield Path(tempdir)
    shutil.rmtree(tempdir)

class TestCpMvRm:
    @pytest.fixture(autouse=True)
    def preparing(self, sandbox_dir):
        self.sandbox = sandbox_dir
        self.runner = CliRunner()
    def test_mv(self):
        #с файлами
        (self.sandbox / 'test.txt').write_text('inf')
        (self.sandbox / 'test2.txt').write_text('')
        result = self.runner.invoke(app, ['mv', str(self.sandbox /'test.txt'), str(self.sandbox / 'test2.txt')])
        assert result.exit_code == 0
        assert os.path.exists(self.sandbox / 'test2.txt')
        assert not os.path.exists(self.sandbox / 'test.txt')
        assert (self.sandbox / 'test2.txt').read_text() == 'inf'
        # каталогами
        new_dir = self.sandbox / 'new_dir'
        new_dir.mkdir(parents=True)
        new_dir2 = self.sandbox / 'new_dir2'
        new_dir2.mkdir(parents=True)
        result = self.runner.invoke(app, ['mv', str(new_dir), str(new_dir2)])
        assert result.exit_code == 0
        assert not os.path.exists(new_dir)
        assert os.path.exists(new_dir2)
        #микс
        new = self.sandbox / "new.txt"
        new.write_text('inf')
        new_dir3 = self.sandbox / 'new_dir3'
        new_dir3.mkdir(parents=True)
        result = self.runner.invoke(app, ['mv', str(new_dir2), str(new), str(new_dir3)])
        assert result.exit_code == 0
        assert os.path.exists(new_dir3 / new)
        assert os.path.exists(new_dir3 / new_dir2)
        # destination не существует, но есть исходный файл
        result = self.runner.invoke(app, ['mv', str(new), "not_exist.txt"])
        assert result.exit_code == 0
        assert not new.exists()
        os.remove('not_exist.txt')

    def test_mv_err(self):
        #источник не существует
        new_dir2 = self.sandbox / 'new_dir2'
        new_dir2.mkdir(parents=True)
        result = self.runner.invoke(app, ['mv', "file.txt", str(new_dir2)])
        assert result.exit_code == 0
        assert 'mv : ошибка' in result.output
        #ошибка, если в источнике несколько файлов, а destination файл
        new = (self.sandbox / "new.txt")
        new.write_text('inf')
        new_dir3 = self.sandbox / 'new_dir3'
        new_dir3.mkdir(parents=True)
        result = self.runner.invoke(app, ['mv', str(new_dir2), str(new_dir3), str(new)])
        assert result.exit_code == 0
        assert 'mv : ошибка' in result.output

    def test_cp(self):
        # копирование одного файла в другой
        (self.sandbox / 'test.txt').write_text('inf')
        (self.sandbox / 'test2.txt').write_text('hello)')
        result = self.runner.invoke(app, ['cp', str(self.sandbox / 'test.txt'), str(self.sandbox / 'test2.txt')])
        assert result.exit_code == 0
        with (self.sandbox / 'test2.txt').open() as f:
            assert f.read() == 'inf'
        # копирование одного файла в другой с -r
        result = self.runner.invoke(app, ['cp', '-r', str(self.sandbox / 'test.txt'), str(self.sandbox / 'test2.txt')])
        assert result.exit_code == 0
        with (self.sandbox / 'test2.txt').open() as f:
            assert f.read() == 'inf'
        #копирование в несуществующий файл
        result = self.runner.invoke(app, ['cp', str(self.sandbox / 'test.txt'), str(self.sandbox / 'test0.txt')])
        assert result.exit_code == 0
        with (self.sandbox / 'test0.txt').open() as f:
            assert f.read() == 'inf'
        #копирование нескольких файлов
        new_dir = self.sandbox / 'new_dir'
        new_dir.mkdir()
        new_dir3 = self.sandbox / 'new_dir3'
        new_dir3.mkdir()
        (self.sandbox / new_dir / "file2.txt").write_text('hello2')
        (self.sandbox / new_dir / "file.txt").write_text('hello')
        result = self.runner.invoke(app, ['cp', str(new_dir / 'file.txt'), str(new_dir / 'file2.txt'), str(new_dir3)])
        assert result.exit_code == 0
        assert (new_dir3 / "file2.txt").exists()
        assert (new_dir3 / "file.txt").exists()
        # копирование директорий с -r
        new_dir2 = self.sandbox / 'new_dir2'
        new_dir2.mkdir()
        result = self.runner.invoke(app, ['cp', '-r', str(new_dir), str(new_dir2)])
        assert result.exit_code == 0
        assert (new_dir2 / "file.txt").exists()
        assert (new_dir2 / "file2.txt").exists()

    def test_cp_err(self):
        # копирование директорий без -r
        new_dir = self.sandbox / 'new_dir'
        new_dir.mkdir()
        new_dir2 = self.sandbox / 'new_dir2'
        new_dir2.mkdir()
        (new_dir / "file.txt").write_text('hello')
        result = self.runner.invoke(app, ['cp', str(new_dir), str(new_dir2)])
        assert result.exit_code == 0
        assert "cp : ошибка" in result.output
        #копирование нескольких файлов в файл
        (new_dir / "file2.txt").write_text('hello')
        (new_dir / "file3.txt").write_text('hello')
        result = self.runner.invoke(app, ['cp', str(new_dir / 'file.txt'), str(new_dir / 'file2.txt'), str(new_dir / 'file3.txt')])
        assert result.exit_code == 0
        assert "cp : ошибка" in result.output

    def test_rm(self, monkeypatch):
        #удаляем файл
        (self.sandbox / 'test.txt').write_text('hello')
        result = self.runner.invoke(app, ['rm', str(self.sandbox / 'test.txt')])
        assert result.exit_code == 0
        assert not os.path.exists(self.sandbox / 'test.txt')
        #удаляем директорию
        new_dir = self.sandbox / 'new_dir'
        new_dir.mkdir()
        monkeypatch.setattr('builtins.input', lambda _: "y")
        result = self.runner.invoke(app, ['rm', "-r", str(self.sandbox / new_dir)])
        assert result.exit_code == 0
        assert not os.path.exists(self.sandbox / new_dir)
        #удаляем несколько файлов
        (self.sandbox / 'test.txt').write_text('hello')
        (self.sandbox / 'test1.txt').write_text('hello')
        result = self.runner.invoke(app, ['rm', str(self.sandbox / 'test.txt'), str(self.sandbox / 'test1.txt')])
        assert result.exit_code == 0
        assert not os.path.exists(self.sandbox / 'test.txt')
        assert not os.path.exists(self.sandbox / 'test1.txt')
    def test_rm_err(self):
        #без -r нельзя удалить каталог
        new_dir = self.sandbox / 'new_dir'
        new_dir.mkdir()
        result = self.runner.invoke(app, ["rm", str(new_dir)])
        assert result.exit_code == 0
        assert "rm : ошибка" in result.output
