import network
wlan=network.WLAN(network.STA_IF)
wlan.active(True)
accesspoints = wlan.scan()
for ap in accesspoints:
    print(ap)
