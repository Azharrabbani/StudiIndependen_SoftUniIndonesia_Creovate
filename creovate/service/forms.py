from django import forms
from .models import Service, ServiceCategory

class AddServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.all(),
        empty_label="Select Category",
        label="Service Category"
    )

    class Meta:
        model = Service
        fields = [
            'title',
            'description',
            'price',
            'service_image',
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'type': 'text',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'type': 'text',
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'type': 'number',
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['service_image'].widget.attrs.update({
            'class': 'form-control',
        })


class UpdateServiceForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=ServiceCategory.objects.all(),
        empty_label="Select Category",
        label="Service Category"
    )

    class Meta:
        model = Service
        fields = [
            'title',
            'description',
            'price',
            'service_image',
            'category',
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['title'].widget.attrs.update({
            'class': 'form-control',
            'type': 'text',
        })
        self.fields['description'].widget.attrs.update({
            'class': 'form-control',
            'type': 'text',
        })
        self.fields['price'].widget.attrs.update({
            'class': 'form-control',
            'type': 'number',
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select',
        })
        self.fields['service_image'].widget.attrs.update({
            'class': 'form-control',
        })