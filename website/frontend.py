"""
Front end GUI
"""
import ipywidgets as widgets
from ipywidgets import Button, HBox, Label, Layout
from IPython.display import display
from website.backend import Prorator


class GUI(object):
    def __init__(self):
        self.allocation = None
        self.input = []
        self.run()

    def add_row(self, button):
        name = widgets.Text(
            value='',
            placeholder='Name',
            disabled=False
        )

        request_amount = widgets.Text(
            value='',
            placeholder='Request Amount',
            disabled=False
        )

        avg_amount = widgets.Text(
            value='',
            placeholder='Average Amount',
            disabled=False
        )

        new_row = [name, request_amount, avg_amount]
        self.input.append(new_row)
        display(HBox(new_row))

    def _prepare_result(self) -> dict:
        m = dict()      # prepare the message
        m['allocation_amount'] = int(self.allocation.value)
        m['investor_amounts'] = []

        for name, rm, am in self.input:
            m['investor_amounts'].append(dict(name=name.value, requested_amount=int(rm.value), average_amount=int(am.value)))
        return m

    def calculate(self, button):
        try:
            input_data = self._prepare_result()
        except ValueError:
            print('Some inputs are not correct, please check and try again!')
            return

        calculate_obj = Prorator(input_data)
        result = calculate_obj.calculate()
        # display result
        print('Results:')
        for name, amount in result.items():
            print('{0} - ${1}'.format(name, round(amount, 5)))

    def run(self):
        label_layout = Layout(width='200px', height='30px')

        self.allocation = widgets.Text(
            value='',
            placeholder='Allocation',
            disabled=False
        )

        display(HBox([Label('Total Available Allocation:', layout=label_layout), self.allocation]))

        add_row_button = widgets.Button(
            description='Add Investor',
            disabled=False,
            button_style='',
            icon='check'
        )
        add_row_button.on_click(self.add_row)

        prorate = widgets.Button(
            description='Prorate',
            disabled=False,
            button_style='',
            icon='check'
        )
        prorate.on_click(self.calculate)
        display(HBox([add_row_button, prorate]))


if __name__ == "__main__":
    print('Done!')
