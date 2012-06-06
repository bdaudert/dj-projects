from django.forms import ModelForm

from my_meta.models import *
from django import forms

class StationMaintenanceForm(ModelForm):
    class Meta:
        model = StationMaintenance
    def save(self):
        data = self.cleaned_data
        sm = StationMaintenance(**data)
        sm.save()


class StationPhysicalForm(ModelForm):
    class Meta:
        model = StationPhysical
    def save(self):
        data = self.cleaned_data
        sp = StationPhysical(**data)
        sp.save()

class StationEquipmentForm(ModelForm):
    class Meta:
        model = StationEquipment
    def save(self):
        data = self.cleaned_data
        se = StationEquipment(**data)
        se.save()

class StationNetworkForm(ModelForm):
    class Meta:
        model = StationNetwork
        exclude = ('begin_date', 'begin_date_flag', 'end_date', 'end_date_flag',)
    def save(self):
        data = self.cleaned_data
        sn = StationNetwork(**data)
        sn.save()

class StationAltNameForm(ModelForm):
    class Meta:
        model = StationAltName
        exclude = ('begin_date', 'begin_date_flag', 'end_date', 'end_date_flag',)
    def save(self):
        data = self.cleaned_data
        san = StationAltName(**data)
        san.save()

class StationDigitalForm(ModelForm):
    class Meta:
        model = StationDigital
        exclude = ('begin_date', 'end_date',)
    def save(self):
        data = self.cleaned_data
        sd = StationDigital(**data)
        sd.save()

class StationClimDivForm(ModelForm):
    class Meta:
        model = StationClimDiv
    def save(self):
        data = self.cleaned_data
        scd = StationClimDiv(**data)
        scd.save()

class ClimDivForm(ModelForm):
    class Meta:
        model = ClimDiv
    def save(self):
        data = self.cleaned_data
        cd = ClimDiv(**data)
        cd.save()

class CountyForm(ModelForm):
    class Meta:
        model = County
        exclude = ('begin_date', 'begin_date_flag', 'end_date', 'end_date_flag',)
    def save(self):
        data = self.cleaned_data
        c = County(**data)
        c.save()

class StationCountyForm(ModelForm):
    class Meta:
        model = StationCounty
        exclude = ('begin_date', 'begin_date_flag', 'end_date', 'end_date_flag',)
    def save(self):
        data = self.cleaned_data
        sc = StationCounty(**data)
        sc.save()

class StationForm(ModelForm):
    class Meta:
        model = Station
    def save(self):
        data = self.cleaned_data
        s = Station(**data)
        s.save()


class StationLocationForm(ModelForm):
    class Meta:
        model = StationLocation
        exclude = ('begin_date', 'begin_date_flag', 'end_date', 'end_date_flag',)
    def save(self):
        data = self.cleaned_data
        sl = StationLocation(**data)
        sl.save()

class VariableForm(ModelForm):
    class Meta:
        model = Variable
        exclude = ('begin_date', 'end_date',)
    def save(self):
        data = self.cleaned_data
        v = Variable(**data)
        v.save()

class StationTimeZoneForm(ModelForm):
    class Meta:
        model = StationTimeZone
        exclude = ('begin_date', 'begin_date_flag', 'end_date', 'end_date_flag',)
    def save(self):
        data = self.cleaned_data
        tz = StationTimeZone(**data)
        tz.save()

class IdTypeForm(ModelForm):
    class Meta:
        model = IdType
    def save(self):
        data = self.cleaned_data
        it = IdType(**data)
        it.save()

class StateForm(ModelForm):
    class Meta:
        model = State
    def save(self):
        data = self.cleaned_data
        st = State(**data)
        st.save()

class StationSubnetworkForm(ModelForm):
    class Meta:
        model = StationSubnetwork
    def save(self):
        data = self.cleaned_data
        ssn = StationSubnetwork(**data)
        ssn.save()

class SubnetworkForm(ModelForm):
    class Meta:
        model = Subnetwork
    def save(self):
        data = self.cleaned_data
        sn = Subnetwork(**data)
        sn.save()

class ZipcodeForm(ModelForm):
    class Meta:
        model = Zipcode
    def save(self):
        data = self.cleaned_data
        zc = Zipcode(**data)
        zc.save()

class NetworkForm(ModelForm):
    class Meta:
        model = Network
    def save(self):
        data = self.cleaned_data
        n = Network(**data)
        n.save()

class StationTimeZoneForm(ModelForm):
    class Meta:
        model = StationTimeZone
    def save(self):
        data = self.cleaned_data
        stz = StationTimeZone(**data)
        stz.save()
