$(document).ready(function ($) {
    $('#id_station_selection, #id_statistic, #id_element').on('change', function(){
        if ($('#app_name').val() != 'sodpiii'){
            $('#form2div').css('display','none');
        }
    });

});
