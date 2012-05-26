from django.forms import ModelForm

from my_meta.models import *
from django import forms

class StationMaintenanceForm(ModelForm):
    class Meta:
        model = StationMaintenance
    def save(self):
        data = self.cleaned_data
        sm = StationMaintenance(**data)
        sm.save(commit=False)


class StationPhysicalForm(ModelForm):
    class Meta:
        model = StationPhysical
    def save(self):
        data = self.cleaned_data
        sp = StationPhysical(**data)
        sp.save(commit=False)

class StationEquipmentForm(ModelForm):
    class Meta:
        model = StationEquipment
    def save(self):
        data = self.cleaned_data
        se = StationEquipment(**data)
        se.save(commit=False)

class StationNetworkForm(ModelForm):
    class Meta:
        model = StationNetwork
    def save(self):
        data = self.cleaned_data
        sn = StationNetwork(**data)
        sn.save(commit=False)

class StationAltNameForm(ModelForm):
    class Meta:
        model = StationAltName
    def save(self):
        data = self.cleaned_data
        san = StationAltName(**data)
        san.save(commit=False)

class StationDigitalForm(ModelForm):
    class Meta:
        model = StationDigital
    def save(self):
        data = self.cleaned_data
        sd = StationDigital(**data)
        sd.save(commit=False)

class StationClimDivForm(ModelForm):
    class Meta:
        model = StationClimDiv
    def save(self):
        data = self.cleaned_data
        scd = StationClimDiv(**data)
        scd.save(commit=False)

class ClimDivForm(ModelForm):
    class Meta:
        model = ClimDiv
    def save(self):
        data = self.cleaned_data
        cd = ClimDiv(**data)
        cd.save(commit=False)

class CountyForm(ModelForm):
    class Meta:
        model = County
    def save(self):
        data = self.cleaned_data
        c = County(**data)
        c.save(commit=False)

class StationCountyForm(ModelForm):
    class Meta:
        model = StationCounty
    def save(self):
        data = self.cleaned_data
        sc = StationCounty(**data)
        sc.save(commit=False)

class StationForm(ModelForm):
    class Meta:
        model = Station
    def save(self):
        data = self.cleaned_data
        s = Station(**data)
        s.save(commit=False)

class StationLocationForm(ModelForm):
    class Meta:
        model = StationLocation
    def save(self):
        data = self.cleaned_data
        sl = StationLocation(**data)
        sl.save(commit=False)

class VariableForm(ModelForm):
    class Meta:
        model = Variable
    def save(self):
        data = self.cleaned_data
        v = Variable(**data)
        v.save(commit=False)

class StationTimeZoneForm(ModelForm):
    class Meta:
        model = StationTimeZone
    def save(self):
        data = self.cleaned_data
        tz = StationTimeZone(**data)
        tz.save(commit=False)

class IdTypeForm(ModelForm):
    class Meta:
        model = IdType
    def save(self):
        data = self.cleaned_data
        it = IdType(**data)
        it.save(commit=False)

class StateForm(ModelForm):
    class Meta:
        model = State
    def save(self):
        data = self.cleaned_data
        st = State(**data)
        st.save(commit=False)

class StationSubnetworkForm(ModelForm):
    class Meta:
        model = StationSubnetwork
    def save(self):
        data = self.cleaned_data
        ssn = StationSubnetwork(**data)
        ssn.save(commit=False)

class SubnetworkForm(ModelForm):
    class Meta:
        model = Subnetwork
    def save(self):
        data = self.cleaned_data
        sn = Subnetwork(**data)
        sn.save(commit=False)

class ZipcodeForm(ModelForm):
    class Meta:
        model = Zipcode
    def save(self):
        data = self.cleaned_data
        zc = Zipcode(**data)
        zc.save(commit=False)

class NetworkForm(ModelForm):
    class Meta:
        model = Network
    def save(self):
        data = self.cleaned_data
        n = Network(**data)
        n.save(commit=False)
