from django import forms


class SearchForm(forms.Form):
    search = forms.TextInput()
    location = forms.SelectMultiple(choices=('test', 'test2', 'test3'))
    date_within = forms.Select(choices=('1 day',
                                        '3 days',
                                        '1 week',
                                        '2 weeks',
                                        '1 month',
                                        '2 months',
                                        '6 months',
                                        '1 year'))
    date = forms.DateInput()
    number_of_trades = forms.NumberInput()
    number_of_trades_filter = forms.Select(choices=('greater than', 'less than'))
    listing_type = forms.RadioSelect(choices=('Selling', 'Buying', 'Trading'))
    payment_type = forms.CheckboxSelectMultiple(choices=('PayPal', 'Local Cash', 'Other'))
