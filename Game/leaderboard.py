## WeirdLand - an arcade shooting game.
## Copyright (c) 2021 moonburnt
##
## This program is free software: you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation, either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program.  If not, see https://www.gnu.org/licenses/gpl-3.0.txt

import json
import logging

log = logging.getLogger(__name__)


class Leaderboard:
    def __init__(self, leaderboard: dict, path=None, sort: bool = True, limit: int = 0):
        if sort:
            for mode in leaderboard:
                leaderboard[mode]["entries"].sort(
                    key=(lambda x: x["score"]),
                    reverse=True,
                )
                if limit:
                    leaderboard[mode]["entries"] = leaderboard[mode]["entries"][:limit]

        self.limit = limit
        self.lb = leaderboard
        self.path = path

    def __iter__(self):
        for var in self.lb:
            yield var

    def __getitem__(self, key):
        return self.lb[key]

    @classmethod
    def from_file(cls, path, sort: bool = True, limit: int = 0):
        with open(path, "r") as f:
            data = json.load(f)
        log.debug(f"Successfully loaded leaderboard from {path}")
        return cls(data, path=path, sort=sort, limit=limit)

    def to_file(self, path=None):
        path = path or self.path
        if not path:
            raise ValueError(f"excepted 'path' kwarg or 'self.path' to be not None")
        with open(path, "w") as f:
            json.dump(self.lb, f)
        log.debug(f"Successfully saved leaderboard into {path}")

    def add_entry(
        self,
        score: int,
        kills: int,
        mode: str,
        username: str = "player",
        limit: int = 0,
    ):
        limit = limit or self.limit

        if not mode in self.lb:
            self.lb[mode] = {}
            self.lb[mode]["slug"] = mode
            self.lb[mode]["entries"] = []
        board = self.lb[mode]["entries"]
        pos = 0
        if board:
            if score < board[-1]["score"]:
                log.debug("Score is less than worst recorded result, ignoring")
                return

            for num, item in enumerate(board):
                if item["score"] < score:
                    pos = num
                    break

        data = {}
        data["name"] = username
        data["score"] = score
        data["kills"] = kills

        board.insert(pos, data)
        if limit:
            self.lb[mode]["entries"] = board[:limit]
