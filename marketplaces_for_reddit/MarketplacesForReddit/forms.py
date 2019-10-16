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
                       ('trading', 'Trading'),
                       ('closed', 'Closed')]
    TRADE_COUNT_FILTERS = [('gt', 'Greater Than'), ('lt', 'Less Than')]
    PAYMENT_TYPES = [('paypal', 'PayPal'), ('cash', 'Local Cash'), ('other', 'Other')]

    search = forms.CharField(label='Search')
    search_title_only = forms.BooleanField(label='Search Title Only')
    location = forms.MultipleChoiceField(label='Locations', choices=LOCATION_CHOICES)
    date_within = forms.ChoiceField(label='Date Within', choices=DATE_WITHIN_CHOICES)
    date = forms.DateField(label='Date')
    number_of_trades = forms.IntegerField()
    number_of_trades_filter = forms.ChoiceField(choices=TRADE_COUNT_FILTERS)
    listing_type = forms.MultipleChoiceField(label='Listing Type', choices=LISTING_CHOICES)
    payment_type = forms.MultipleChoiceField(choices=PAYMENT_TYPES)

