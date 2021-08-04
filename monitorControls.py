import raildriver

rd = raildriver.RailDriver()
rd.set_rail_driver_connected(True)  # start data exchange
loco_name = rd.get_loco_name()
print(loco_name)

controls = rd.get_controller_list()
for control in controls:
    print(control[1])