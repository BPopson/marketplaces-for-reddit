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
    TRADE_COUNT_FILTERS = [('gt', 'Greater Than'),
                           ('lt', 'Less Than')]
    PAYMENT_TYPES = [('paypal', 'PayPal'),
                     ('cash', 'Local Cash'),
                     ('other', 'Other')]

    search = forms.CharField(label='Search',
                             required=False)
    search_title_only = forms.BooleanField(label='Search Title Only',
                                           required=False)
    location = forms.MultipleChoiceField(label='Locations',
                                         choices=LOCATION_CHOICES,
                                         required=True)
    date_within = forms.ChoiceField(label='Date Within',
                                    choices=DATE_WITHIN_CHOICES,
                                    initial=14,
                                    required=True)
    date = forms.DateField(label='Date',
                           required=False)
    number_of_trades = forms.IntegerField(required=True)
    number_of_trades_filter = forms.ChoiceField(choices=TRADE_COUNT_FILTERS,
                                                required=False)
    listing_type = forms.MultipleChoiceField(label='Listing Type',
                                             choices=LISTING_CHOICES,
                                             required=True)
    payment_type = forms.MultipleChoiceField(choices=PAYMENT_TYPES,
                                             required=True)

    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        # Add form-control for bootstrap to all visible fields
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'
        # TODO: See about moving this out of the constructor for this form
        self.fields['search_title_only'].widget.attrs['class'] = 'form-check-input'
