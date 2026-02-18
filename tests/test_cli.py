import os
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from src.starray.cli import cmd_init, _resolve_config_path


class TestCliConfigResolution(unittest.TestCase):
    def test_resolve_config_prefers_explicit_path(self) -> None:
        with TemporaryDirectory() as tmp:
            explicit = Path(tmp) / "custom.toml"
            resolved = _resolve_config_path(str(explicit))
            self.assertEqual(resolved, explicit)

    def test_resolve_config_uses_env_then_user_then_project(self) -> None:
        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            env_config = tmp_path / "env.toml"
            env_config.write_text("[provider]\nname='openai'\n", encoding="utf-8")

            old_cwd = Path.cwd()
            os.chdir(tmp_path)
            old_xdg_config_home = os.environ.get("XDG_CONFIG_HOME")
            old_starray_config = os.environ.get("STARRAY_CONFIG")
            try:
                os.environ["STARRAY_CONFIG"] = str(env_config)
                resolved = _resolve_config_path(None)
                self.assertEqual(resolved, env_config)

                del os.environ["STARRAY_CONFIG"]
                os.environ["XDG_CONFIG_HOME"] = str(tmp_path / "xdg")
                user_cfg = Path(os.environ["XDG_CONFIG_HOME"]) / "starray" / "starray.toml"
                user_cfg.parent.mkdir(parents=True, exist_ok=True)
                user_cfg.write_text("[provider]\nname='openai'\n", encoding="utf-8")
                resolved = _resolve_config_path(None)
                self.assertEqual(resolved, user_cfg)

                user_cfg.unlink()
                project_cfg = Path("configs") / "starray.toml"
                project_cfg.parent.mkdir(parents=True, exist_ok=True)
                project_cfg.write_text("[provider]\nname='openai'\n", encoding="utf-8")
                resolved = _resolve_config_path(None)
                self.assertEqual(resolved, project_cfg)
            finally:
                os.chdir(old_cwd)
                if old_xdg_config_home is None:
                    os.environ.pop("XDG_CONFIG_HOME", None)
                else:
                    os.environ["XDG_CONFIG_HOME"] = old_xdg_config_home
                if old_starray_config is None:
                    os.environ.pop("STARRAY_CONFIG", None)
                else:
                    os.environ["STARRAY_CONFIG"] = old_starray_config


class TestCliInit(unittest.TestCase):
    def test_init_writes_config(self) -> None:
        with TemporaryDirectory() as tmp:
            cfg = Path(tmp) / "starray.toml"
            rc = cmd_init(cfg, force=False)
            self.assertEqual(rc, 0)
            self.assertTrue(cfg.exists())
            text = cfg.read_text(encoding="utf-8")
            self.assertIn("[provider]", text)
            self.assertIn("[storage]", text)


if __name__ == "__main__":
    unittest.main()
