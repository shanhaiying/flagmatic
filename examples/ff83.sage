P = ThreeGraphProblem(6, forbid="5:123124345")
C = ThreeGraphBlowupConstruction("3:123")
P.set_extremal_construction(C)
P.solve_sdp()
P.make_exact()