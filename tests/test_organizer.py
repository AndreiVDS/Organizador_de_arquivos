from pathlib import Path

from organizador.categories import Categories, DEFAULT
from organizador.organizer import apply, plan


def make(folder: Path, *names: str) -> None:
    for n in names:
        (folder / n).write_text("x", encoding="utf-8")


def test_plan_lists_moves_without_touching_disk(tmp_path):
    make(tmp_path, "a.pdf", "b.png", "notes.txt")
    cats = Categories.build(DEFAULT)

    moves = plan(tmp_path, cats)

    assert {m.src.name for m in moves} == {"a.pdf", "b.png", "notes.txt"}
    assert (tmp_path / "a.pdf").exists()          # nothing moved yet
    assert not (tmp_path / "PDF").exists()


def test_apply_moves_into_category_folders(tmp_path):
    make(tmp_path, "a.pdf", "b.png", "b2.png", "weird.xyz")
    cats = Categories.build(DEFAULT)

    moved = apply(plan(tmp_path, cats), dry_run=False)

    assert moved == 4
    assert (tmp_path / "PDF" / "a.pdf").is_file()
    assert (tmp_path / "Imagens" / "b.png").is_file()
    assert (tmp_path / "Imagens" / "b2.png").is_file()
    assert (tmp_path / "outros" / "weird.xyz").is_file()
    assert not (tmp_path / "a.pdf").exists()


def test_dry_run_changes_nothing(tmp_path):
    make(tmp_path, "a.pdf")
    moved = apply(plan(tmp_path, Categories.build(DEFAULT)), dry_run=True)
    assert moved == 1
    assert (tmp_path / "a.pdf").exists()
    assert not (tmp_path / "PDF").exists()


def test_name_clash_is_not_overwritten(tmp_path):
    (tmp_path / "PDF").mkdir()
    (tmp_path / "PDF" / "a.pdf").write_text("original", encoding="utf-8")
    (tmp_path / "a.pdf").write_text("new", encoding="utf-8")

    apply(plan(tmp_path, Categories.build(DEFAULT)), dry_run=False)

    assert (tmp_path / "PDF" / "a.pdf").read_text() == "original"
    assert (tmp_path / "PDF" / "a (1).pdf").read_text() == "new"


def test_second_run_is_idempotent(tmp_path):
    make(tmp_path, "a.pdf")
    cats = Categories.build(DEFAULT)
    apply(plan(tmp_path, cats), dry_run=False)
    again = apply(plan(tmp_path, cats, recursive=True), dry_run=False)
    assert again == 0
