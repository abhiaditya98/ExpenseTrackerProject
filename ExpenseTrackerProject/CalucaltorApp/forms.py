from django import forms

class CaluclatorForm(forms.Form):

    num1  = forms.FloatField(label = "Number1",required = True)
    num2 = forms.FloatField(label = "Number2",required = True)

    def clean(self):
        cleaned_data =  super().clean()
        n1 = cleaned_data.get("num1")
        n2 = cleaned_data.get("num2")

        try:
            float(n1)
            float(n2)
        except ValueError:
            print(f"{ValueError}")
        return cleaned_data