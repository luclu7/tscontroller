import PySimpleGUI as sg
from serial import *
import raildriver
from threading import Thread

sg.theme('Dark')  # Add a touch of color

read_button = sg.ReadFormButton('VACMA', button_color=('white', sg.theme_element_background_color(color='black')),
                                border_width=5, bind_return_key=True)
VA_text = sg.Text('VACMA', border_width=5, size=(30, 1), font=("Helvetica", 25), text_color='green')
RegulatorScale = sg.ProgressBar(1, orientation="h", size=(20,20), key='regulator')

layout = [[sg.Text("VACMA: ", text_color='white'), VA_text],
          [sg.Text("Regulator: ", text_color='white'), RegulatorScale],
          [sg.Button('Ok'), sg.Cancel()]]

# Create the window
window = sg.Window("Demo", layout, finalize=True)
VacmaPrevValue, RegulatorPrevValue = 0, 0


rd = raildriver.RailDriver()
rd.set_rail_driver_connected(True)  # start data exchange
loco_name = rd.get_loco_name()

# Create an event loop
with Serial(port='COM46', baudrate=115200, timeout=1, writeTimeout=1) as port_serie:
    if port_serie.isOpen():
        while True:
            ligne = port_serie.readline().rstrip()
            args = ligne.split(",".encode())
            try:
                # print(("Regulator: " + args[0].decode("utf-8")))
                # print(("Reverser: " + args[1].decode("utf-8")))
                if args[2] != VacmaPrevValue:
                    print("VACMA: " + args[2].decode("utf-8"))
                    VacmaPrevValue = args[2]
                    if args[2] == b'1':
                        VA_text.Update("Maintenue", text_color="green")
                    else:
                        VA_text.Update("Lâché", text_color="red")
                    window.finalize()

                if (args[0] != RegulatorPrevValue):
                    print("Regulator: " + args[0].decode("utf-8"))
                    RegulatorPrevValue = args[0]
                    window['regulator'].update_bar(float(args[0].decode("utf-8")))
                    window.finalize()

                # rd.set_controller_value("Regulator", float(args[0]))
                # rd.set_controller_value('Reverser', float(args[1]))
                # rd.set_controller_value("CommandeVacma", float(args[2].decode("utf-8")))
            except ValueError:
                print("ValueError")
                print(args)
            except IndexError:
                print("IndexError")
                print(args)


window.close()