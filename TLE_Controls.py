import flet as ft


class Widget2(ft.Card):
    def __init__(self, name, value, send_uart_tla):
        super().__init__()
        self.value = value
        self.tla = name
        self.name = name
        self.test = name
        self.inc = 1
        self.send_uart_tla = send_uart_tla
        self.display_value = ft.Text(
            value,
            color="pink600",
            theme_style=ft.TextThemeStyle.BODY_SMALL
            # bgcolor="blue600"
        )
        self.inc_minus_button = ft.FilledTonalButton(text=f"-{self.inc}", on_click=self.send_inc_minus, visible=False)
        self.inc_plus_button = ft.FilledTonalButton(text=f"+{self.inc}", on_click=self.send_inc_add, visible=False)
        self.minus_button = ft.FilledTonalButton(text="-", on_click=self.send_minus, visible=False)
        self.plus_button = ft.FilledTonalButton(text="+", on_click=self.send_add, visible=False)
        self.title = ft.ListTile(
            title=ft.Text(name, color="black600", theme_style=ft.TextThemeStyle.BODY_SMALL, visible=True),
            subtitle=ft.Text("", color="black600", theme_style=ft.TextThemeStyle.BODY_SMALL, visible=False),
            dense=True,
            visible=True,
        )
        self.value = ft.Row(
            [self.display_value],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.START,
            visible=True,
            spacing=0
        )
        self.actions = ft.Row(
            [],
            visible=False
        )
        self.subtitle = ft.Text("", color="black600", visible=False)
        self.command_button = ft.FilledTonalButton(text=f"{self.name}", on_click=self.send_command, visible=False)
        self.display_label = ft.Text(name, color="green600", visible=False)
        self.content = ft.Container(
            content=ft.Column(
                [
                    self.title,
                    # self.subtitle,
                    self.value,
                    self.actions
                ],
                horizontal_alignment=ft.CrossAxisAlignment.START,
                spacing=0
            ),
            padding=5
        )
        print(f'NEW WIDGET :: {self.name}')

    def set_type(self, widget_type):
        if widget_type == 'VARIABLE':
            self.actions.controls = [
                self.inc_minus_button,
                self.minus_button,
                self.plus_button,
                self.inc_plus_button
            ]
            self.value.visible = True
            self.title.visible = True
            self.actions.visible = True
            self.plus_button.visible = True
            self.minus_button.visible = True
            self.update()
            return

        if widget_type == 'COMMAND':
            self.value.visible = False
            self.title.visible = False
            self.command_button.visible = True
            self.actions.controls = [self.command_button]
            self.actions.visible = True
            self.update()
            return

        if widget_type == 'LITERAL':
            self.title.visible = True
            self.value.visible = True
            self.display_value.theme_style = ft.TextThemeStyle.BODY_MEDIUM
            self.update()

    def update_title(self, value):
        print(f'Update {self.name} {value}')
        self.title.title.value = value
        self.display_label.value = value
        self.update()

    def update_subtitle(self, value):
        print(f'Update Sub Title')
        self.title.subtitle.value = value
        self.title.subtitle.visible = True
        self.display_label.value = value
        self.update()

    def clear_subtitle(self):
        print(f'Clear Sub Title')
        self.title.subtitle.visible = False
        self.update()

    def update_value(self, value):
        print(f'Update Value {self.name} {value}')
        self.display_value.value = value
        self.update()

    def update_value_colour(self, value):
        print(f'Update Value Colour {self.name}, {value}')
        self.display_value.color = value
        self.update()

    def update_inc(self, value):
        print(f'Update Increment {self.name} {value}')
        self.inc = value
        self.inc_minus_button.visible = True
        self.inc_minus_button.text = f'-{self.inc}'
        self.inc_plus_button.visible = True
        self.inc_plus_button.text = f'+{self.inc}'
        self.update()

    def update_button_text(self, text):
        self.command_button.text = text
        self.update()

    def send_add(self, e):
        print(f'Send TLA +')
        self.send_uart_tla(e, f'{self.name}+1\r')

    def send_inc_add(self, e):
        print(f'Send TLA +')
        self.send_uart_tla(e, f'{self.name}+{self.inc}\r')

    def send_minus(self, e):
        print(f'Send TLA -')
        self.send_uart_tla(e, f'{self.name}-1\r')

    def send_inc_minus(self, e):
        print(f'Send TLA -')
        self.send_uart_tla(e, f'{self.name}-{self.inc}\r')

    def send_command(self, e):
        print(f'Send Command TLA -')
        self.send_uart_tla(e, f'{self.tla}-{self.inc}\r')
