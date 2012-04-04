"""

flagmatic 2

Copyright (c) 2012, E. R. Vaughan. All rights reserved.

Redistribution and use in source and binary forms, with or without modification,
are permitted provided that the following conditions are met:

1) Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2) Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation and/or
other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

from sage.rings.all import Integer

from problem import *
from flag import *
from flag_misc import *

class AxiomsProblem(Problem):
	
	def __init__(self, r=3, oriented=False):
	
		Problem.__init__(self, r, oriented)
		self._density_graphs = []


	def calculate_densities(self):
		pass
	

	def set_density_graph(self, dg):
		pass

	
	def set_density_graphs(self, dgs):
		pass


	def set_density_edge_number(self, k, ne):
		pass


	def clear_axioms(self):
		
		self._axioms = []
		self._axiom_flags = []
		self._densities = []


	def add_axiom(self, tg, terms):

		m = self.n - max([t[0].n for t in terms]) + tg.n

		axiom_flags = generate_flags(m, tg, self._r, self._oriented,
			forbidden_edge_numbers=self._forbidden_edge_numbers,
			forbidden_graphs=self._forbidden_graphs,
			forbidden_induced_graphs=self._forbidden_induced_graphs)
		
		num_densities = len(axiom_flags)
		sys.stdout.write("Added %d quantum graphs.\n" % num_densities)
		
		num_graphs = len(self._graphs)
		quantum_graphs = [[Integer(0) for i in range(num_graphs)] for j in range(num_densities)]
		
		axiom_flags_block = make_graph_block(axiom_flags, m)
		graph_block = make_graph_block(self._graphs, self.n)

		for i in range(len(terms)):
			fg = terms[i][0]
			flags_block = make_graph_block([fg], fg.n)
			rarray = flag_products(graph_block, tg, flags_block, axiom_flags_block)
			for row in rarray:
				gi = row[0]
				j = row[1] # always 0
				k = row[2]
				value = Integer(row[3]) / Integer(row[4])
				quantum_graphs[k][gi] += value * terms[i][1]
		
		self._axioms.append((tg, terms))
		self._axiom_flags.append(axiom_flags)
		self._densities.extend(quantum_graphs)
	
	
	def add_codegree_axiom(self, value):

		if not self.r == 3:
			raise NotImplementedError
	
		tg = Flag("2:")
		f1 = Flag("3:123(2)")
		f2 = Flag("2:(2)")
		self.add_axiom(tg, [(f1, Integer(1)), (f2, -value)])


	def add_degree_axiom(self, value):
	
		if self.oriented:
			raise NotImplementedError
	
		if self.r == 3:
	
			tg = Flag("1:")
			f1 = Flag("3:123(1)")
			f2 = Flag("1:(1)")
			self.add_axiom(tg, [(f1, Integer(1)), (f2, -value)])

		elif self.r == 2:

			tg = Flag("1:", 2)
			f1 = Flag("2:12(1)", 2)
			f2 = Flag("1:(1)", 2)
			self.add_axiom(tg, [(f1, Integer(1)), (f2, -value)])
		
	
	def add_out_degree_axiom(self, value):
	
		if not (self.r == 2 and self.oriented):
			raise NotImplementedError
	
		tg = Flag("1:", 2, True)
		f1 = Flag("2:12(1)", 2, True)
		f2 = Flag("1:(1)", 2, True)
		self.add_axiom(tg, [(f1, Integer(1)), (f2, -value)])


	def add_in_degree_axiom(self, value):
	
		if not (self.r == 2 and self.oriented):
			raise NotImplementedError
	
		tg = Flag("1:", 2, True)
		f1 = Flag("2:21(1)", 2, True)
		f2 = Flag("1:(1)", 2, True)
		self.add_axiom(tg, [(f1, Integer(1)), (f2, -value)])	
		