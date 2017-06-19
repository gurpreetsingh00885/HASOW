from django import forms


class RenameForm(forms.Form):
	def __init__(self, applianc, *args,**kwargs):
		#self.get_field('appliance').initial=applianc
		super(RenameForm,self).__init__(*args,**kwargs)
	new_name = forms.CharField(label='', max_length=10)
	appliance = forms.CharField(label= '', max_length=10, required=False)
	
	def save(self, name):
		self.fields['appliance'].initial=name
		
	