from django import forms
from django.forms import ModelForm

from my_meta.models import *


class StationMaintenanceForm(forms.Form):
    ucan_station_id = forms.IntegerField(widget=forms.widgets.HiddenInput)
    maintenance_date = forms.DateField()
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 50, 'rows': 18}))

    def save(self):
        data = self.cleaned_data
        sm = StationMaintenance(**data)
        sm.save()


class StationPhysicalForm(forms.Form):
    ucan_station_id = forms.IntegerField(widget=forms.widgets.HiddenInput)
    slope = forms.IntegerField()
    aspect = forms.IntegerField()
    gps = forms.CharField(max_length=1)
    site_description = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))
    route_directions = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        sp = StationPhysical(**data)
        sp.save()

class StationEquipmentForm(forms.Form):
    ucan_station_id = forms.IntegerField(widget=forms.widgets.HiddenInput)
    equipment_type = forms.CharField(max_length=30)
    eq_manufacturer = forms.CharField(max_length=30)
    eq_model = forms.CharField(max_length=20)
    serial_num = forms.CharField(max_length=20)
    eq_description = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))
    install_date = forms.DateField()
    remove_date = forms.DateField(required=False)
    ref_height = forms.IntegerField()
    sampling_interval = forms.CharField(max_length=10)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        se = StationEquipment(**data)
        se.save()

class StationNetworkForm(forms.Form):
    ucan_station_id = forms.IntegerField(widget=forms.widgets.HiddenInput)
    network_station_id = forms.CharField(max_length=20)
    id_type = forms.IntegerField() #FIX ME: this is foreign key: IdType : id_type_key Q: int or [int] char e.g., [6] GHCN ID
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_code = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        sn = StationNetwork(**data)
        sn.save()

class StationAltNameForm(forms.Form):
    ucan_station_id = forms.IntegerField(widget=forms.widgets.HiddenInput)
    station_alt_name = forms.CharField(max_length=30)
    name_type_key = forms.IntegerField()
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_code = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        san = StationAltName(**data)
        san.save()

class StationDigitalForm(forms.Form):
    ucan_station_id = forms.IntegerField(widget=forms.widgets.HiddenInput)
    network_station_id = forms.CharField(max_length=20)
    network = forms.IntegerField()  #FIX ME: this is foreign key: Network : network_key
    begin_date = forms.DateField()
    end_date = forms.DateField()

    def save(self):
        data = self.cleaned_data
        sd = StationDigital(**data)
        sd.save()

class StationClimDivForm(forms.Form):
    clim_div_key = forms.IntegerField() #pk = True ?? If so, this shouldn't show up in ucan_id table list ??? FIX ME: something's up
    clim_div_code = forms.CharField(max_length=2)
    fips_state_code = forms.CharField(max_length=2)
    fips_state_abbr = forms.CharField(max_length=2)
    ncdc_state_code = forms.CharField(max_length=2)
    clim_div_name = forms.CharField(max_length=30)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        scd = StationClimDiv(**data)
        scd.save()

class ClimDivForm(forms.Form):
    clim_div_key = forms.IntegerField() #pk
    clim_div_code = forms.CharField(max_length=2)
    fips_state_code = forms.CharField(max_length=2)
    fips_state_abbr = forms.CharField(max_length=2)
    ncdc_state_code = forms.CharField(max_length=2)
    clim_div_name = forms.CharField(max_length=30)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        cd = ClimDiv(**data)
        cd.save()

class CountyForm(forms.Form):
    county_key = forms.IntegerField() #pk
    fips_state_code = forms.CharField(max_length=2)
    fips_state_abbr = forms.CharField(max_length=2)
    fips_county_code = forms.CharField(max_length=3)
    county_name = forms.CharField(max_length=31)
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        c = County(**data)
        c.save()

class StationCountyForm(forms.Form):
    ucan_station_id = forms.IntegerField() # Not the real pk
    county = forms.IntegerField() #foreign key: County : county_key
    fips_state_code =  forms.CharField(max_length=2)
    fips_county_code = forms.CharField(max_length=3)
    county_name = forms.CharField(max_length=31)
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_code = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        sc = StationCounty(**data)
        sc.save()

class StationForm(forms.Form):
    ucan_station_id = forms.IntegerField() #pk
    station_best_name = forms.CharField(max_length=30)
    country_key = forms.IntegerField()
    fips_country_code = forms.CharField(max_length=2)
    state = forms.IntegerField() #foreign key: State : state_key
    fips_state_abbr = forms.CharField(max_length=2)
    fips_state_code = forms.CharField(max_length=2)
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_code = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

class StationLocationForm(forms.Form):
    ucan_station_id = forms.IntegerField() # Not the real pk
    longitude = forms.FloatField()
    latitude =  forms.FloatField()
    unit_key = forms.IntegerField()
    best_elevation = forms.FloatField()
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_flag = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        sl = StationLocation(**data)
        sl.save()

class VariableForm(forms.Form):
    ucan_station_id = forms.IntegerField() # Not the real pk
    network_station_id = forms.CharField(max_length=20)
    network = forms.IntegerField() #foreign key: Network : network_key
    var_major_id = forms.IntegerField()
    var_minor_id = forms.IntegerField()
    begin_date = forms.DateField()
    end_date = forms.DateField()

    def save(self):
        data = self.cleaned_data
        v = Variable(**data)
        v.save()

class StationTimeZoneForm(forms.Form):
    ucan_station_id = forms.IntegerField() # Not the real pk
    time_zone = forms.FloatField()
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_code = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        tz = StationTimeZone(**data)
        tz.save()

class IdTypeForm(forms.Form):
    id_type_key = forms.IntegerField() #pk
    name = forms.CharField(max_length=30)
    description = forms.CharField(max_length=254)
    controller_info = forms.CharField(max_length=50)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        it = IdType(**data)
        it.save()

class StateForm(forms.Form):
    state_key = forms.IntegerField() #pk
    country_key = forms.IntegerField()
    fips_country_abbr = forms.CharField(max_length=2)
    fips_state_code =   forms.CharField(max_length=2)
    ncdc_state_code =   forms.CharField(max_length=2)
    fips_state_abbr =   forms.CharField(max_length=2)
    state_name = forms.CharField(max_length=30)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        st = State(**data)
        st.save()
class StationSubnetworkForm(forms.Form):
    subnetwork_key = forms.IntegerField() #pk
    ucan_station_id = forms.IntegerField()
    network_station_id = forms.CharField(max_length=20)

    def save(self):
        data = self.cleaned_data
        ssn = StationSubnetwork(**data)
        ssn.save()

class SubnetworkForm(forms.Form):
    subnetwork_key = forms.IntegerField() #pk
    network_key = forms.IntegerField()
    network_subnetwork_id = forms.CharField(max_length=16)
    subnetwork_name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        sn = Subnetwork(**data)
        sn.save()

class ZipcodeForm(forms.Form):
    zipcode = forms.CharField(max_length=5) #pk
    longitude = forms.FloatField()
    latitude =  forms.FloatField()

    def save(self):
        data = self.cleaned_data
        zc = Zipcode(**data)
        zc.save()

class NetworkForm(forms.Form):
    network_key = forms.IntegerField() #pk
    network_code = forms.CharField(max_length=8)
    name = forms.CharField(max_length=30)
    description = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))
    id_type = forms.IntegerField() #foreign key : IdType : id_type_key
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(widget=forms.widgets.Textarea({'cols': 36, 'rows': 8}))

    def save(self):
        data = self.cleaned_data
        n = Network(**data)
        n.save()
