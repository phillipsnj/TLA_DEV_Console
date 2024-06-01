import flet as ft
import solo_uart
from TLE_Controls import Widget, Widget2


class ConfigApp(ft.UserControl):
    def __init__(self, port):
        super().__init__()
        self.UART = solo_uart.SoloUART(port, self.process_input, self.process_output)
        self.UART.start()
        self.tla_controls = {}
        self.controls_list = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        self.messages_list = ft.ListView(expand=1, spacing=5, padding=10, auto_scroll=True)
        self.refresh_button = ft.FilledButton(
            text="Refresh",
            on_click=self.refresh_screen
        )
        self.clear_button = ft.FilledButton(
            text="Clear",
            on_click=self.clear_messages,
        )
        self.user_message_button = ft.FilledButton(
            text="Send",
            on_click=self.process_output
        )
        self.user_message = ft.TextField(
            expand=1,
            bgcolor=ft.colors.WHITE
        )
        self.user_message_row = ft.Row([
            self.user_message,
            self.user_message_button,
            self.clear_button
        ])
        self.control_action_row = ft.Row([
            self.refresh_button
        ])
        self.control_view = ft.Container(
            width=350,
            height=380,
            content=self.controls_list,
            margin=10,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
        )
        self.control_action = ft.Container(
            width=350,
            height=60,
            content=self.control_action_row,
            margin=10,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
        )
        self.message_view = ft.Container(
            width=350,
            height=380,
            content=self.messages_list,
            margin=10,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
        )
        self.message_action = ft.Container(
            width=350,
            height=60,
            content=self.user_message_row,
            margin=10,
            padding=10,
            bgcolor=ft.colors.WHITE,
            border_radius=10,
        )

    def build(self):
        return ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        self.control_view,
                        self.control_action
                    ]),
                ft.Column(
                    controls=[
                        self.message_view,
                        self.message_action,
                    ]),
            ])

    def process_input(self, msg):  # TLS Message Received from Device
        print("incoming msg : " + str(msg))
        self.messages_list.controls.append(ft.Text(f"{msg}", color="blue600"))
        tla = msg[:3]
        if len(msg) > 3:
            operator = msg[3]
            value = msg[4:].replace(',\r', '')
        else:
            operator = ""
            value = ""
        if tla in self.tla_controls:
            self.update_control(tla, operator, value)
        else:
            self.create_control(tla, operator, value)
        self.update()

    def update_control(self, tla, operator, value):
        if operator == '~':
            self.tla_controls[tla].update_value(value)
            return
        elif operator == '=':
            self.tla_controls[tla].update_value(value)
            return
        if operator == ':':
            action_operator = value[:3]
            action_value = value[4:]
            if action_operator == "CNM":
                self.tla_controls[tla].update_text(action_value)
            elif action_operator == "INC":
                self.tla_controls[tla].update_inc(action_value)
            elif action_operator == "TYP":
                self.tla_controls[tla].set_type(action_value)
            elif action_operator == "BNT":
                self.tla_controls[tla].update_button_text(action_value)
            elif action_operator == "CLR":
                self.tla_controls[tla].update_value_colour(action_value)
        elif operator == '%':
            pass
        else:
            pass

    def create_control(self, tla, operator, value):
        print(f'Create Control {tla} {operator} {value}')
        if operator == '=':
            print(f'Create Literal {tla}')
            self.tla_controls[tla] = Widget2(tla, value, self.on_click_send_tla)
            self.controls_list.controls.append(self.tla_controls[tla])

    def process_output(self, e):
        print("outgoing msg : " + str(self.user_message.value))
        self.messages_list.controls.append(ft.Text(f"{self.user_message.value}", color="pink600"))
        self.UART.send(self.user_message.value + "\r")
        self.update()

    def clear_messages(self, e):
        self.messages_list.clean()

    def refresh_screen(self, e):
        self.messages_list.clean()
        self.controls_list.clean()
        self.tla_controls = {}
        # self.UART.send("INF\r")
        self.send_tla('INF')

    def send_tla(self, tla):
        print(f'Send TLA {tla}')
        self.messages_list.controls.append(ft.Text(f"{tla}", color="pink600"))
        self.UART.send(tla + "\r")

    def on_click_send_tla(self, e, tla):
        print(f'On Click Send TLA {tla}')
        self.messages_list.controls.append(ft.Text(f"{tla}", color="pink600"))
        self.UART.send(tla + "\r")
        self.update()


def main(page: ft.Page):
    # create application instance
    port = '/dev/tty.usbserial-0001'
    page.title = "TLA Development Console Class"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    page.vertical_alignment = ft.MainAxisAlignment.START
    page.bgcolor = ft.colors.GREY_200
    config_app = ConfigApp(port)
    page.add(config_app)


ft.app(target=main)
