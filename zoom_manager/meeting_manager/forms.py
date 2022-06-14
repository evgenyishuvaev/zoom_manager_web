from django import forms


class CreateMeetingForms(forms.Form):
    host_id = forms.CharField(label="Аккаунт", max_length=100)
    topic = forms.CharField(label="Тема", max_length=100)
    sheduled_date = forms.Field(label="Когда", widget=forms.DateInput(attrs={"type": "date"}))
    sheduled_time = forms.Field(label="На какое время", widget=forms.TimeInput(attrs={"type": "time"}))
    duration = forms.Field(label="Продолжительность", widget=forms.TimeInput(attrs={"type": "time"}))
    is_record_to_cloud = forms.CharField(label="Автоматически записывать конференцию в облако", widget=forms.CheckboxInput)