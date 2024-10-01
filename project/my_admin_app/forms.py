from django import forms

class CSVUploadForm(forms.Form):
    guide_csv_file = forms.FileField()
    student_csv_file=forms.FileField()
    start_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label='Start Date'
    )
    end_date = forms.DateField(
        widget=forms.TextInput(attrs={'type': 'date'}),
        label='End Date'
    )
