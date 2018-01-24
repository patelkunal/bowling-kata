#!/usr/bin/env python3

from random import randint
from uuid import uuid4


class Frame(object):
  """
  Frame maintains the state of player's performance during his/her turn, like knocks in each try
  """
  TOTAL_PINS = 10
  
  def __init__(self, total_pins: int = TOTAL_PINS):
    self._knock_counter = 0
    self._total_pins = total_pins
    self._standing_pins = self._total_pins
    # initialize knocks (based on min_tries) with empty list
    self.knocks = []
    
  def knock(self, hits: int = 0) -> int:
    """ player knocks and state gets updated within Frame and that happens here !! """
    if self._knock_counter >= 2:
      raise ValueError("no one can try more than twice !!")
    elif hits > self._standing_pins or hits > self._total_pins:
      raise ValueError("you cannot knock more than what's available !!")
    else:
      self._knock_counter += 1
    
    return self._do_knock(hits)

  def _do_knock(self, hits: int) -> int:
    """ adjust self._standing_pins and update self.knocks list """
    self._standing_pins -= hits
    self.knocks.append(hits)
    return self._standing_pins

  def get_knocks(self) -> list:
    """ returns the knocks within a Frame for scorer to calculate the score"""
    return self.knocks

  def get_knock_counter(self):
    """returns knock_counter which denotes the times player has tried knocking the current Frame"""
    return self._knock_counter

  def __str__(self):
    return "Frame<{}>".format(', '.join(map(str, self.knocks)))


class Turn(object):
  """
  wrapper for Frame instance to keep track of Frames in each instance. because of spare and strike
  its possible to have two frames in each player turn
  """
  def __init__(self):
    self._frame = Frame()
    self._bonus_frame = None
    pass

  def bonus_frame(self) -> Frame:
    self._bonus_frame = Frame()
    return self._bonus_frame

  def get_bonus_frame(self) -> Frame:
    return self._bonus_frame

  def any_bonus_frame(self):
    return self._bonus_frame is not None

  def get_frame(self) -> Frame:
    return self._frame

  def __str__(self):
    if self.any_bonus_frame():
      return "[{}, {}]".format(self._frame, self._bonus_frame)
    return "[{}]".format(self._frame)


class Scorer:
  @staticmethod
  def turn_score(turn: Turn) -> int:
    _frame = turn.get_frame()
    _frame_score = Scorer.score(_frame)
    
    if turn.any_bonus_frame():
      # _frame_score will be 10 in case of spare/strike
      _bonus_frame = turn.get_bonus_frame()
      if GameRuleEngine.is_spare(_frame):
        return _frame_score + _bonus_frame.get_knocks()[0] + Scorer.score(_bonus_frame)
      elif GameRuleEngine.is_strike(_frame):
        return _frame_score + Scorer.score(_bonus_frame) + Scorer.score(_bonus_frame)
    else:
      return _frame_score

  @staticmethod
  def score(f: Frame) -> int:
    return sum(f.get_knocks())
  pass # end-of-class-Scorer


class GameRuleEngine:
  
  STRIKE_BONUS_POINTS = 10
  SPARE_BONUS_POINTS = 5

  @staticmethod
  def is_strike(f: Frame) -> bool:
    """ checks if the given Frame is strike or not"""
    return f.get_knock_counter() == 1 and f.get_knocks()[0] == Frame.TOTAL_PINS

  @staticmethod
  def is_spare(f: Frame) -> bool:
    """ checks if the given Frame is spare or not"""
    return f.get_knock_counter() == 2 and sum(f.get_knocks()) == Frame.TOTAL_PINS


class Player():
  """
  actor in game who plays/knocks the pins in Frame.
  Consumes a fresh Frame instance and return the same instance after playing.

  TODO - first version will only let player try two knocks - spare/strike based logic in next version
  """
  def __init__(self, name):
    self.name = name
    self._id = str(uuid4())

  def __str__(self):
    return "Player[id = {}, name = {}]".format(self._id, self.name) 

  def __hash__(self):
    return self._id

  def __eq__(self, other):
    if isinstance(self, other.__class__):
      return self._id == other._id
    return False

  def play(self, f: Frame = Frame()) -> Frame:
    """
    player takes a frame and returns the same frame after playing
    """
    remaining_pins: int = f.knock(randint(0, Frame.TOTAL_PINS))
    if remaining_pins != 0:
      f.knock(randint(0, remaining_pins))
    return f # end-of-def-play
  # end-of-class-Player


class Game(object):
  def __init__(self, player):
    self._player = player
    self._turns = list()

  def play(self):
    _t: Turn = Turn()
    _f: Frame = self._player.play(_t.get_frame())
    _final_score: int = 0
    if GameRuleEngine.is_strike(_f):
      print("BINGO !! its a strike !!")
      _bonus_frame = self._player.play(_t.bonus_frame())
      _final_score = Scorer.turn_score(_t)
    elif GameRuleEngine.is_spare(_f):
      print("YEY !! its a spare !!")
      _bonus_frame = self._player.play(_t.bonus_frame())
      _final_score = Scorer.turn_score(_t)
    else:
      _final_score = Scorer.score(_f)
    _pair = (_t, _final_score)
    self._turns.append(_pair)
    return _pair
  
  def __str__(self):
    _ts = ' | '.join(["{} -> {}".format(_[0], _[1]) for _ in self._turns])
    return "{} --> turns ==> {}".format(self._player.name, _ts)
  pass # end-of-class-Game


class KataBowlingGame(object):
  TOTAL_TURNS: int = 5
  def __init__(self, player_names: list):
    self._game = Game(Player(player_names[0]))

  def start_tournament(self):
    for _turn in range(0, self.TOTAL_TURNS):
      print("****************TURN_SCORE******************************")
      self._game.play()
      print(self._game)
    print("****************FINAL_SCORE******************************")
    print(self._game)


if __name__ == "__main__":
  _kgb = KataBowlingGame(["kunal"])
  _kgb.start_tournament()
  pass # end-of-main

