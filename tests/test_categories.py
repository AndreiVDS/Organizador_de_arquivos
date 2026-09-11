import json

from organizador.categories import Categories, DEFAULT


def test_folder_for_known_and_unknown():
    cats = Categories.build(DEFAULT)
    assert cats.folder_for("foto.JPG") == "Imagens"
    assert cats.folder_for("script.py") == "Códigos"
    assert cats.folder_for("weird.xyz") == "outros"


def test_only_filters_categories():
    cats = Categories.build(DEFAULT, only={"imagem"})
    assert cats.folder_for("a.png") == "Imagens"
    assert cats.folder_for("a.pdf") == "outros"  # pdf category excluded
    assert cats.known_keys == ["imagem"]


def test_from_json(tmp_path):
    f = tmp_path / "c.json"
    f.write_text(json.dumps({"livros": {"folder": "Livros", "extensions": [".epub", ".mobi"]}}))
    cats = Categories.from_json(f)
    assert cats.folder_for("book.epub") == "Livros"
    assert "Livros" in cats.folder_names
