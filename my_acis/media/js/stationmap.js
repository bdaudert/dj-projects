// Path to the blank image should point to a valid location on your server
Ext.BLANK_IMAGE_URL = 'http://www.wrcc.dri.edu/media/ext/images/default/s.gif';


/***
    GMapPanelCluster extends the GMapPanel extension to use a the MarkerClusterer.
***/
Ext.ux.GMapPanelCluster = Ext.extend(Ext.ux.GMapPanel, {
    markerCluster : null,
    initComponent : function(){
        Ext.ux.GMapPanelCluster.superclass.initComponent.call(this);        
    },
    /**
     * Remove markers from the array that is passed in.
     */
    removeMarkers : function(markers) {
        return this.markerCluster.removeMarkers(markers);
    },
    /**
     * Creates markers from the array that is passed in.
     */
    addMarkers : function(markers) {
        if (this.markerCluster === null) {
            this.markerCluster = new MarkerClusterer(this.gmap,[],this.clusterOptions);
        }
        if (Ext.isArray(markers)){
            this.markerCluster.addMarkers(markers);
        }
    }
});
Ext.reg('gmappanelcluster',Ext.ux.GMapPanelCluster); 


/***
    StationMap pulls everything together: a clustered map inside of an
    Ext panel with toolbar/menu.
***/
function StationMap(config) {

    var that = this; // keep a self-reference in scope

    this.map_panel = new Ext.ux.GMapPanelCluster({
        gmapType: 'map',
        id: 'map_panel',
        height: config['map_height'] || 600,
        zoomLevel: config['zoom_level'] || 4,
        mapControls: config['mapControls'] || ['GSmallMapControl'],
        setCenter: config['center'] || { lat: 39, lng: -102 },
        clusterOptions: config['clusterOptions'] || {
            maxZoom: 8 }
    });

    var ICON_COLORS = config['icon_colors'] || [
                                                 '#ff0000' // red
                                                ,'#00ff00' // green
                                                ,'#0000ff' // blue
                                                ,'#ffff00' // yellow
                                                ,'#ff00ff' // fuschia
                                                ,'#00ffff' // teal
                                                ,'#ff8800' // orange
                                                ,'#990000' // dark red
                                                ,'#009900' // dark green
                                                ,'#000099' // dark blue
                                                ,'#000000' // black
                                                ,'#888888' // grey
                                                ,'#cccccc' // light grey
                                                ,'#ffffff' // white
                                                ];

    var styled_icons = [];
    var icon_index = 0;
    for (var i = 0,c; c=ICON_COLORS[i]; i++) {
        styled_icons.push( new StyledIcon(StyledIconTypes.MARKER, {color: c}) );
    }

    // show the stations by default (onload)?
    if ('checked_by_default' in config) this.checked_by_default = config['checked_by_default'];
    else this.checked_by_default = false; // default false

    if ('show_invert_selected' in config) this.show_invert_selected = config['show_invert_selected'];
    else this.show_invert_selected = true; // default true

    if ('fill_station_grid' in config) this.fill_station_grid = config['fill_station_grid'];
    else this.fill_station_grid = false; // default false 

    // create a single infobox that will move around to each marker
    this.infobox = config['infobox'] || new InfoBox({ pixelOffset: new google.maps.Size(-123, -8) });

    this.networks_shown = [];
    this.station_store = new Ext.data.JsonStore({
        autoLoad: true,
        url: config['station_json_url'],
        root: 'stations',
        stn_markers: {}, // Populates from data file. Station 'types' are used as keys to list of station markers.
        stn_icons: {},
        fields: [
            {name:'name', type:'string'}
            ,'state'
            ,'networks'
            ,{name:'lat',type:'float'}
            ,{name:'lng',type:'float'}
            ,{name:'elevation',type: 'float'}
            ,{name:'start_date', type: 'string'}
            ,{name:'end_date', type: 'string'}
            ,{name:'elements'}
        ],
        listeners: {
            'load': function(store, records, options) {
                        Ext.each(records, function(s) {
                            if ( s.data['lat'] && s.data['lng'] ) {
                                Ext.each(s.data['networks'] || [['Unknown','Unknown','']], function(n) {
                                    if ( !(n[0] in store.stn_markers) ) {
                                        store.stn_markers[n[0]] = [];
                                        store.stn_icons[n[0]] = styled_icons[icon_index%ICON_COLORS.length];
                                        icon_index++;
                                    }

                                    // create a new map marker
                                    var marker = that.createStationMarker(n, s.data);
                                    s['marker'] = marker;

                                    // attach marker's click event to the markerClick function
                                    google.maps.event.addListener(marker, 'click', function(){ that.markerClick(this) });

                                    // Add marker to list of each type
                                    store.stn_markers[n[0]].push(marker);
                                });
                            }
                        });

                        // Add marker lists to map
                        if ( that.checked_by_default ) that.addMarkersToMap();

                        // Update the map_panel's toolbar
                        that.updateToolbar();

                        // clear the grid
                        if ( !that.fill_station_grid ) {
                            store.filterBy(function(r){return false;});
                        }

                    } // end JsonStore 'load' event
        } // end JsonStore listeners
    });  // end JsonStore

    this.toolbar = new Ext.Toolbar({
        id: 'toolbar',
        items: [
            new Ext.Button({
                text: 'Options',
                menu: this.getOptionsMenu(config)
            })
        ]
    });
    this.station_grid = new Ext.grid.GridPanel({
        id: 'station_grid',
        store: this.station_store,
        title: config['grid_panel_title'] || '',
        width: config['grid_width'] || '100%',
        height: config['grid_height'] || 400,
        colModel: new Ext.grid.ColumnModel({
            defaults: {
                width: 120,
                sortable: true
            },
            // Store fields: ['name','state','lat','lng','elevation','networks'],
            columns: [
                {header: 'Name', width: 240, dataIndex: 'name'},
                {header: 'State', width: 60, dataIndex: 'state'},
                {header: 'Lat', dataIndex: 'lat'},
                {header: 'Lon', dataIndex: 'lng'},
                {header: 'Elevation', dataIndex: 'elevation'},
                {header: 'Start', dataIndex: 'start_date'},
                {header: 'End',   dataIndex: 'end_date'},
                {header: 'Networks', dataIndex: 'networks', renderer: this.renderNetworks}
            ]
        }),
        sm: new Ext.grid.RowSelectionModel({ singleSelect:true }),
        listeners: { rowclick: function(grid, rowIndex, evt) { that.rowClick(grid, rowIndex)}},
        viewConfig: { forceFit: true }
    }); // end station_grid

    this.main_panel = new Ext.Panel({
        id: 'main_panel',
        renderTo: "id_map_window",
        title: config['panel_title'] || '',
        width: config['panel_width'] || '100%',
        height: config['panel_height'] || '100%',
        items: [ this.toolbar, this.map_panel, this.station_grid]
    });

} // end StationMap


StationMap.prototype.getStyleIcon = function(stn_type, stn_data) {
    return this.station_store.stn_icons[stn_type];
};

StationMap.prototype.renderNetworks = function(networks) {
    if ( networks != null ) {
        var s = [];
        for ( var n in networks ) {
            if (networks[n][0]) s.push(networks[n][0]);
        }
        return s.join(', ');
    }
    return "Unknown";
};

StationMap.prototype.rowClick = function(grid, i) {
    var record = grid.store.getAt(i);
    this.highlightMarker(record.marker);
};

StationMap.prototype.highlightMarker = function(marker) {
    // make sure the marker's network is checked
    var networks = marker.stn_data['networks'];
    for ( var i=0, n; n = networks[i]; i++ ) {
            var menu = Ext.getCmp("menu_item_"+n[0]);
            menu.setChecked(true);
    }
    // move the map to the marker
    var map = this.map_panel.getMap();
    map.setZoom(10);
    marker.setVisible(true);
    map.panTo(marker.getPosition());
    // 'click' marker to show infowindow, etc.
    this.markerClick(marker);
};

StationMap.prototype.createStationMarker = function(stn_network, stn_data) {
    if ( stn_data['networks'] === null ) {
        stn_data['networks'] = [stn_network];
    }
    var marker = new StyledMarker({
        styleIcon: this.getStyleIcon(stn_network[0], stn_data),
        flat: true, // don't show shadow
        title: stn_data['name'],
        stn_data: stn_data, // keep stn_data with marker object
        position: new google.maps.LatLng(parseFloat(stn_data['lat']), parseFloat(stn_data['lng']))
    });
    return marker;
};

StationMap.prototype.addMarkersToMap = function() {
    for (var n in this.station_store.stn_markers) {
        this.map_panel.addMarkers(this.station_store.stn_markers[n]);
    }
};

StationMap.prototype.updateToolbar = function() {
    // Add a 'Networks' menu
    this.toolbar.add(new Ext.Button({
        text: 'Networks',
        menu: this.getNetworksMenu()
    }));
    this.toolbar.doLayout(); // refresh toolbar
};

StationMap.prototype.checkNetworksMenuItem = function(network, checked){
    var that = this;
    var markers = this.station_store.stn_markers[network];
    if ( checked ) {
        this.map_panel.addMarkers(markers);
        this.networks_shown.push(network);
    } else {
        this.map_panel.removeMarkers(markers);
        this.networks_shown.remove(network);
    }

    // if we only show selected networks in the grid...
    this.toggleFilterGrid( Ext.getCmp('id_option_display_all').checked );
};

StationMap.prototype.toggleFilterGrid = function(show) {
    var that = this;
    if ( show ) {
        this.station_store.clearFilter();
    } else {
        this.station_store.filterBy(function(r){
            var networks = r.get('networks');
            var ret = false;
            for ( var i=0,n; n=networks[i]; i++ ) {
                if (n[0]) ret = ret || that.networks_shown.indexOf(n[0]) !== -1;
            }
            return ret;
        });
    }
}

StationMap.prototype.getNetworksMenu = function() {
    var that = this;
    var network_menu = new Ext.menu.Menu();
    for (var n in this.station_store.stn_markers) {
        var icon_url = StyledIconTypes.MARKER.getURL(this.station_store.stn_icons[n]);
        // replace url with a scaled version
        // see: http://groups.google.com/group/google-chart-api/web/chart-types-for-map-pins
        icon_url = icon_url.replace(/d_map_pin_letter&chld=/,'d_map_spin&chld=0.25|0');
        var item = new Ext.menu.CheckItem({
            checked: that.checked_by_default,
            id: "menu_item_"+n,
            text: n,
            style: "background-image: url(\ "+icon_url+");",
            listeners: {
                checkchange: function(item,checked) {
                    that.checkNetworksMenuItem(item.text, checked)
                }
            }
        });
        network_menu.add(item);
    }
    // Add 'invert selected' option
    if ( this.show_invert_selected ) {
        network_menu.add( new Ext.menu.Item({
            text: "Invert Selected",
            listeners: {
                click: function(item, e){
                    Ext.each(network_menu.items.items, function(i){
                        if ( i != item )
                            i.setChecked(!i.checked);
                    });
                }
            }
        }));
    }

    return network_menu;
};

StationMap.prototype.getOptionsMenu = function(config){
    var that = this;
    var options_menu = new Ext.menu.Menu({
        items: [
            new Ext.menu.CheckItem({
                id: 'id_option_display_all',
                text: 'Display all stations in table',
                checked: config['initial_option_display_all'] || false,
                listeners: {
                    checkchange: function(item,checked){
                        that.toggleFilterGrid(checked);
                    }
                }
            })
        ]
    });
    return options_menu;
};

StationMap.prototype.markerClick = function(marker) {
    this.infobox.setOptions({
        content: this.getInfoWindowContent(marker.stn_data),
    });
    this.infobox.open(this.map_panel.getMap(), marker);
};

StationMap.prototype.getNetworkLink = function(n, stn_data) {
    /* Returns a URL for a given network tuple. */
    var s = "";

    if ( n[0] == "RAWS" || n[0] == "CDEC" || n[0] == "CIMIS" || n[0] == "DRI" || n[0] == "NDBC" ) {
        s += "http://raws.dri.edu/cgi-bin/rawMAIN.pl?";
        s += (stn_data['state'] || 'ca').toLowerCase();
        s += n[2];
    }
    if ( n[0] == "NWS COOP" ) {
        s += "http://wrcc.dri.edu/cgi-bin/cliMAIN.pl?";
        s += (stn_data['state'] || 'ca').toLowerCase();
        s += n[2].substring(2);
    }
    if ( n[0] == "ICAO" ) {
        s += "http://www.wrcc.dri.edu/cgi-bin/rawMAIN.pl?";
        s += (stn_data['state'] || 'ca').toLowerCase();
        s += n[2];
    }

    return s
};

StationMap.prototype.getInfoWindowContent = function(stn_data) {
    var s = "";
    s += "<div>";

    s += "<h3>" + stn_data['name'] + "</h3>";

    for ( var i=0, n; n = stn_data['networks'][i]; i++ ) {
        if ( n[0] !== "Unknown" ) {
            s += '<p>' + n[0] + ": ";
            var url = this.getNetworkLink(n, stn_data);
            if (url) { s += '<a href="' + url + '" target="_blank">' + n[2] + "</a>"; }
            else { s += n[2]; }
            s += '</p>';
        }
    }

    if ( "elevation" in stn_data ) {
        s += "<p>Elevation: " + stn_data['elevation'] + " ft.</p>";
    }

    // Check for a function that inserts elements
    if ( typeof this.getElementInfo == "function" ) {
        s += this.getElementInfo(stn_data);
    }
    s += "</div>";

    return s
};
