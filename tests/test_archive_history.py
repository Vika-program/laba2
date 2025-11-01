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

class TestArchive:
    @pytest.fixture(autouse=True)
    def preparing(self, sandbox_dir):
        self.sandbox = sandbox_dir
        self.runner = CliRunner()
    def test_zip_unzip(self):
        dir = self.sandbox / 'dir'
        os.mkdir(dir)
        (dir / 'test.txt').write_text('inf')
        result = self.runner.invoke(app, ['zip', str(dir), str(self.sandbox / 'archive')])
        assert result.exit_code == 0
        assert os.path.exists(self.sandbox / 'archive')

        new_dir = self.sandbox / "new_dir"
        os.mkdir(new_dir)
        (new_dir / 'test2.txt').write_text('')
        result = self.runner.invoke(app, ['zip', str(new_dir)])
        assert result.exit_code == 0
        assert os.path.exists('folder')

        result = self.runner.invoke(app, ['unzip', str(self.sandbox / 'archive')])
        assert result.exit_code == 0
        assert os.path.exists(self.sandbox / 'dir')
        #пытаемся распаковать не архив
        result = self.runner.invoke(app, ['unzip', str(self.sandbox / 'dir')])
        assert "unzip : ошибка" in result.output

    def test_tar_untar(self):
        dir = self.sandbox / 'dir'
        os.mkdir(dir)
        (dir / 'test.txt').write_text('inf')
        result = self.runner.invoke(app, ['tar', str(dir), str(self.sandbox / 'archive')])
        assert result.exit_code == 0
        assert os.path.exists(self.sandbox / 'archive')

        new_dir = self.sandbox / "new_dir"
        os.mkdir(new_dir)
        (new_dir / 'test2.txt').write_text('')
        result = self.runner.invoke(app, ['tar', str(new_dir)])
        assert result.exit_code == 0
        assert os.path.exists('folder')

        result = self.runner.invoke(app, ['untar', str(self.sandbox / 'archive')])
        assert result.exit_code == 0
        assert os.path.exists(self.sandbox / 'dir')
        # пытаемся распаковать не архив
        result = self.runner.invoke(app, ['untar', str(self.sandbox / 'dir')])
        assert "untar : ошибка" in result.output
        shutil.rmtree('tmp')
        os.remove("folder")
        shutil.rmtree("dir")


class TestHistory:
    def setup_method(self):
        self.runner = CliRunner()

    def test_history(self):
        result = self.runner.invoke(app, ['history'])
        assert result.exit_code == 0
        n = 5
        with open('.history', 'r') as file:
            lines = file.readlines()
            for i in range(len(lines) - n, len(lines)):
                line = lines[i].rstrip()
                assert line in result.output

        result = self.runner.invoke(app, ['history', '10'])
        assert result.exit_code == 0
        n = 10
        with open('.history', 'r') as file:
            lines = file.readlines()
            for i in range(len(lines) - n, len(lines)):
                line = lines[i].rstrip()
                assert line in result.output
