from django import forms


class SearchForm(forms.Form):
    DATE_WITHIN_CHOICES = [('1', '1 day'),
                           ('3', '3 days'),
                           ('7', '1 week'),
                           ('14', '2 weeks'),
                           ('30', '1 month'),
                           ('60', '2 months'),
                           ('180', '6 months'),
                           ('365', '1 year')]
    LOCATION_CHOICES = [('USA', '[USA]'),
                        ('CAN', '[CAN]')]
    LISTING_CHOICES = [('selling', 'Selling'),
                       ('buying', 'Buying'),
                       ('trading', 'Trading')]
    search = forms.CharField()
    location = forms.MultipleChoiceField(choices=LOCATION_CHOICES)
    date_within = forms.ChoiceField(choices=DATE_WITHIN_CHOICES)
    date = forms.DateField(input_formats=['%Y-%m-%d'])
    number_of_trades = forms.NumberInput()
    number_of_trades_filter = forms.Select(choices=('greater than', 'less than'))
    listing_type = forms.ChoiceField(choices=LISTING_CHOICES, widget=forms.RadioSelect)
    payment_type = forms.CheckboxSelectMultiple(choices=('PayPal', 'Local Cash', 'Other'))
