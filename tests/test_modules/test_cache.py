import pytest
from modules.cache import Bdfs_Cache 


def test_bdfs_cache(capsys):
    cache = Bdfs_Cache()
    assert {} == cache.getStorage()


def test_setData(capsys):
    cache = Bdfs_Cache()
    cache.setData()
    captured = capsys.readouterr()
    assert "setData" in captured.out


def test_unsetData(capsys):
    cache = Bdfs_Cache()
    cache.unsetData()
    captured = capsys.readouterr()
    assert "unsetData" in captured.out


def test_udpate(capsys):
    cache = Bdfs_Cache()
    cache.update()
    captured = capsys.readouterr()
    assert "update" in captured.out

def test_get(capsys):
    cache = Bdfs_Cache()
    cache.get()
    captured = capsys.readouterr()
    assert "get" in captured.out


def test_clear(capsys):
    cache = Bdfs_Cache()
    cache.clear()
    captured = capsys.readouterr()
    assert "clear" in captured.out

def test_delete(capsys):
    cache = Bdfs_Cache()
    cache.delete()
    captured = capsys.readouterr()
    assert "delete" in captured.out

def test_write(capsys):
    cache = Bdfs_Cache()
    cache.insert()
    captured = capsys.readouterr()
    assert "insert" in captured.out
    assert "write" in captured.out