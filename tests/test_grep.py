import pytest
import tempfile
import shutil
from pathlib import Path
from typer.testing import CliRunner
from src.main import app

@pytest.fixture
def sandbox_dir():
    tempdir = tempfile.mkdtemp()
    yield Path(tempdir)
    shutil.rmtree(tempdir)

class TestGrep:
    @pytest.fixture(autouse=True)
    def preparing(self, sandbox_dir):
        self.sandbox = sandbox_dir
        self.runner = CliRunner()
    def test_grep(self):
        dir_test = (self.sandbox / "dir_test")
        dir_test.mkdir()
        (dir_test / "test.txt").write_text("test hello goodbye")
        result = self.runner.invoke(app, ["grep", "hello", str(dir_test / "test.txt")])
        assert result.exit_code == 0
        assert "hello" in result.output

        result = self.runner.invoke(app, ["grep", '-i', "Hello", str(dir_test / "test.txt")])
        assert result.exit_code == 0
        assert "hello" in result.output

        result = self.runner.invoke(app, ["grep", "*.txt", str(dir_test)])
        assert result.exit_code == 0
        assert 'test.txt' in result.output

        path = self.sandbox / "1 level" / "2 level" / "3 level" / "test.txt"
        path.parent.mkdir(parents=True)
        (self.sandbox / "1 level" / "2 level" / "3 level" / "test.txt").write_text("test hello goodbye")
        (self.sandbox / "1 level" / "2 level" / "3 level" / "test.txt").write_text("plane apple goodbye")
        result = self.runner.invoke(app, ["grep", "-r", "[a-z]{5}", str(self.sandbox / "1 level")])
        assert result.exit_code == 0
        assert "plane" in result.output
        assert "goodb" in result.output
        assert "apple" in result.output

        result = self.runner.invoke(app, ["grep", "-r", "-i", "APPLE", str(self.sandbox / "1 level")])
        assert result.exit_code == 0
        assert "apple" in result.output
