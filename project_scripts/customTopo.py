#sudo mn --custom /home/milo/customTopo.py --topo=mytopo
from mininet.topo import Topo
class MyTopo( Topo ):
    def __init__(self):
        Topo.__init__( self )

        Host1 = self.addHost('h1')
        Host2 = self.addHost('h2')
        Host3 = self.addHost('h3')

        Switch1 = self.addSwitch("s1")

        self.addLink(Host1, Switch1)
        self.addLink(Host2, Switch1)
        self.addLink(Host3, Switch1)

topos = {'mytopo': (lambda: MyTopo())}
