from django import forms


class QuizForm(forms.Form):
    def __init__(self, question, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["answer"] = forms.ChoiceField(
            label=question.text,
            choices=[
                ("a", question.option_a),
                ("b", question.option_b),
                ("c", question.option_c),
                ("d", question.option_d),
            ],
            widget=forms.RadioSelect,
        )
