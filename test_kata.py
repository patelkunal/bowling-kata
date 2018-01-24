import pytest
from unittest import mock
from kata import Player, Scorer, Frame, Turn, GameRuleEngine, Game

def test_player_and_scorer():
  player = Player('kunal')
  assert player.name == 'kunal'
  assert player._id is not None
  with mock.patch("kata.randint", return_value=2):
    f: Frame = player.play()
    knocks = f.get_knocks()
    assert 2 == knocks[0]
    assert 2 == knocks[1]
    assert 4 == Scorer.score(f)
  pass


def test_frame_and_scorer():
  f = Frame()
  f.knock(2)
  with pytest.raises(ValueError):
    f.knock(10)
  f.knock(3)
  assert 5 == Scorer.score(f)
  with pytest.raises(ValueError):
    f.knock(5)
  
  strike_frame = Frame()
  strike_frame.knock(10)
  assert 10 == Scorer.score(strike_frame)
  with pytest.raises(ValueError):
    strike_frame.knock(1)
  pass


def test_turn_and_scorer():
  t = Turn()
  f = t.get_frame()
  assert f is not None
  assert not t.any_bonus_frame()
  bonus_frame = t.bonus_frame()
  assert bonus_frame is not None
  assert t.any_bonus_frame()

  f.knock(10)
  bonus_frame.knock(10)
  assert 30 == Scorer.turn_score(t)


def test_game():
  print()
  with mock.patch("kata.randint", side_effect = [2, 7]):
    print("testing non-spare and non-strike !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 9
    assert not GameRuleEngine.is_spare(_turn.get_frame())
    assert not GameRuleEngine.is_strike(_turn.get_frame())
    print()

  with mock.patch("kata.randint", side_effect = [3, 7, 1, 4]) as m:
    print("testing spare !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 16 # (3 + 7) + 1(first_knock_from_second_try) + (1 + 4)
    assert GameRuleEngine.is_spare(_turn.get_frame())
    assert not GameRuleEngine.is_strike(_turn.get_frame())
    print()
  with mock.patch("kata.randint", side_effect = [3, 7, 5, 5]) as m:
    print("testing spare !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 25 # (3 + 7) + 5(first_knock_from_second_try) + (5 + 5)
    assert GameRuleEngine.is_spare(_turn.get_frame())
    assert not GameRuleEngine.is_strike(_turn.get_frame())
    print()
  with mock.patch("kata.randint", side_effect = [3, 7, 10]) as m:
    print("testing spare !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 30 # (3 + 7) + 10(first_knock_from_second_try) + (10)
    assert GameRuleEngine.is_spare(_turn.get_frame())
    assert not GameRuleEngine.is_strike(_turn.get_frame())
    print()

  with mock.patch("kata.randint", side_effect = [10, 7, 1]) as m:
    print("testing strike !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 26 # (10) + (7 + 1)(knocks_from_second_try) + (7 + 1)
    assert not GameRuleEngine.is_spare(_turn.get_frame())
    assert GameRuleEngine.is_strike(_turn.get_frame())
    print()
  with mock.patch("kata.randint", side_effect = [10, 5, 5]) as m:
    print("testing strike !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 30 # (10) + (5 + 5)(knocks_from_second_try) + (5 + 5)
    assert not GameRuleEngine.is_spare(_turn.get_frame())
    assert GameRuleEngine.is_strike(_turn.get_frame())
    print()
  with mock.patch("kata.randint", side_effect = [10, 10]) as m:
    print("testing strike !!")
    _g = Game(Player("kunal"))
    _turn, _turn_score = _g.play()
    print("{} -> {}".format(_turn, _turn_score))
    assert _turn_score == 30 # (10) + 10 (knocks_from_second_try) + (10)
    assert not GameRuleEngine.is_spare(_turn.get_frame())
    assert GameRuleEngine.is_strike(_turn.get_frame())
    print()

