from organizador.cli import main


def test_cli_dry_run(tmp_path, caplog):
    (tmp_path / "a.pdf").write_text("x", encoding="utf-8")
    rc = main([str(tmp_path), "--dry-run"])
    assert rc == 0
    assert (tmp_path / "a.pdf").exists()


def test_cli_sorts(tmp_path):
    (tmp_path / "a.pdf").write_text("x", encoding="utf-8")
    (tmp_path / "b.png").write_text("x", encoding="utf-8")
    assert main([str(tmp_path)]) == 0
    assert (tmp_path / "PDF" / "a.pdf").is_file()
    assert (tmp_path / "Imagens" / "b.png").is_file()


def test_cli_rejects_missing_folder(tmp_path):
    assert main([str(tmp_path / "nope")]) == 2
