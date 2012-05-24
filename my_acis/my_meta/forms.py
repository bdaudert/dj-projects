from django import forms

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
    id_type = forms.IntegerField()
    begin_date_flag = forms.CharField(max_length=2)
    begin_date = forms.DateField()
    end_date_flag = forms.CharField(max_length=2)
    end_date = forms.DateField()
    history_flag = forms.CharField(max_length=2)
    src_quality_code = forms.CharField(max_length=5)
    last_updated = forms.DateField()
    updated_by = forms.CharField(max_length=8)
    remark = forms.CharField(max_length=254)

    #def save(self):
    #    data = self.cleaned_data
    #    sn = StationNetwork(**data)
    #    sn.save()

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
    remark = forms.CharField(max_length=254)

    #def save(self):
    #    data = self.cleaned_data
    #    san = StationAltName(**data)
    #    san.save()
