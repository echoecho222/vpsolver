"""
This code is part of the Arc-flow Vector Packing Solver (VPSolver).

Copyright (C) 2013-2015, Filipe Brandao
Faculdade de Ciencias, Universidade do Porto
Porto, Portugal. All rights reserved. E-mail: <fdabrandao@dcc.fc.up.pt>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

from .... import *
from utils import *

class CmdSet:
    def __init__(self):
        self.defs = ""
        self.data = ""

    def __getitem__(self, name):
        return lambda *args: self.evalcmd(name, args)

    def evalcmd(self, name, args):
        assert len(args) == 1
        values = args[0]
        self.defs += ampl_set(name, values)[0]

class CmdParam:
    def __init__(self):
        self.defs = ""
        self.data = ""

    def __getitem__(self, name):
        return lambda *args: self.evalcmd(name, args)

    def evalcmd(self, name, args):
        assert len(args) == 1
        values = args[0]
        if type(values) in [list, dict]:
            match = re.match("\s*("+rgx_varname+")\s*({"+rgx_varname+"})?\s*", name)
            assert match != None
            name, index = match.groups()
        else:
            match = re.match("\s*("+rgx_varname+")\s*", name)
            assert match != None
            name, index = match.group(0), None
        if index == None:
            index = name+"_I"
        else:
            index = index.strip('{} ')
        name = name.strip()
        if type(values) == list:
            values = list2dict(values)
        if type(values) == dict:
            self.defs += ampl_set(index, values.keys())[0]
        pdefs, pdata = ampl_param(name, index, values)
        self.defs += pdefs
        self.data += pdata
