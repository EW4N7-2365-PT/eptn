import matplotlib
import wntr
import matplotlib.pylab as plt

wn = wntr.network.WaterNetworkModel('network.inp')
sim = wntr.sim.EpanetSimulator(wn)

wn.options.time.duration = 12 * 60 * 60
wn.options.time.hydraulic_timestep = 15 * 60
wn.options.time.report_timestep = 15 * 60

wn.write_inpfile('inpt.inp')

wn = wntr.network.WaterNetworkModel('inpt.inp')
wn.options.quality.mode = 'AGE'
sim = wntr.sim.EpanetSimulator(wn)

results = sim.run_sim()
# pressure_at_5h = results.node['pressure'].loc[5 * 3600, :]
# print(results.node['pressure'].to_json('hell.json'))
# print(results.node.keys())

pressure = results.node['pressure']
#
# t1 = wntr.graphics.plot_network(wn, node_size=30, node_attribute=pressure,
#                                 title='Pressure at 5 hours')
#
# plt.savefig('testo.png')
# print(t1)
#
for node in wn.node_name_list:
    rec = pressure.loc[:, node]
    fig = plt.figure()
    ax = plt.gca()
    plt.xlabel('time')
    plt.ylabel('pressure')
    formatter = matplotlib.ticker.FuncFormatter(lambda ms, x: ms // (60 * 60))
    ax.xaxis.set_major_formatter(formatter)
    rec.plot(legend=False, grid=True, ax=ax, linewidth=2).get_figure()
    fig.savefig(f'ret/{node}.png')
