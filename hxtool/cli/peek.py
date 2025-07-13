# -*- coding: ascii -*-

from argparse import ArgumentError

from .poke import PokeCommand


class PeekCommand(PokeCommand):

    name = "peek"

    def run(self):
        if self.args.data:
            raise ArgumentError(None, f"Cannot write data with peek command; use poke")

        return super().run()
