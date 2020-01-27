from django import forms


class SearchListForm(forms.Form):
    platform_choices = (
        ('PC', 'PC'),
        ('PS4', 'PS4'),
        ('XONE', 'Xbox One'),
        ('Switch', 'Nintendo switch')
    )
    genre_choices = (
        ('Strategy', 'Strategy'),
        ('Shooter', 'Shooter'),
        ('Role-playing (RPG)', 'RPG'),
        ('Platform', 'Platformer')
    )
    platforms = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple(),
                                          choices=platform_choices)
    genres = forms.MultipleChoiceField(
        choices=genre_choices, widget=forms.CheckboxSelectMultiple)
    rating_lower_limit = forms.IntegerField(min_value=0, max_value=100)
    rating_upper_limit = forms.IntegerField(min_value=0, max_value=100)


class SearchNameForm(forms.Form):
    name = forms.CharField(max_length=100)