"""Simulators are used to sweep over different fiber parameters,
and to solve for modes using those parameters.

Main implementation of the simulator is in
:class:`~fibermodes.simulator.simulator.Simulator`. Subclasses can be used
for performing different kind of smulations; e.g. for running simulations
in parallel using multiple processes, or even using MPI.

"""