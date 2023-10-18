import header
import networkx as nx
import matplotlib.pyplot as plt

with open("./result_json/topology_data.json", 'r') as f: 
    topology_data=header.json.load(f)


g1=nx.Graph()
g2=nx.Graph()




routers=topology_data.keys()

for router in routers:
    g1.add_node(router)
    g2.add_node(router)

    router_connect_lst=topology_data[router]['Connectivity']['Router'].keys()
    terminal_connect_lst=topology_data[router]['Connectivity']['Terminal'].keys()

    for r_connect in router_connect_lst:
        g1.add_edge(router,r_connect)
        g2.add_edge(router,r_connect)
    
    for t_connect in terminal_connect_lst:
        g1.add_edge(router,t_connect)

pos1=nx.kamada_kawai_layout(g1)
pos2=nx.kamada_kawai_layout(g2)

plt.figure(figsize=(20,20))
plt.subplot(211)
nx.draw_networkx(g1,pos1,with_labels=True)
plt.subplot(212)
nx.draw_networkx(g2,pos1,with_labels=True)

plt.show()