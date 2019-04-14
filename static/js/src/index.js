import $ from '../node_modules/jquery/dist/jquery.min.js';
import '../node_modules/bootstrap/dist/js/bootstrap.min.js';
import '../../css/sass/main.scss';
import '../../css/less/styles.less';

function rad2degr(rad) { return rad * 180 / Math.PI; }
function degr2rad(degr) { return degr * Math.PI / 180; }

/**
 * @param latLngInDeg array of arrays with latitude and longtitude
 *   pairs in degrees. e.g. [[latitude1, longtitude1], [latitude2
 *   [longtitude2] ...]
 *
 * @return array with the center latitude longtitude pairs in
 *   degrees.
 */
 function render_zoom(lat, lon){
     let map = new Datamap({
        element: document.getElementById('map'), fills: {
            defaultFill: '#0B5091' //the keys in this object map to the "fillKey" of [data] or [bubbles]
        },
        done: function(datamap){
            console.log(datamap);
            datamap.svg.selectAll('.datamaps-subunit').on('click',
            country_info
        )},
        geographyConfig: {
            dataUrl: null, //if not null, datamaps will fetch the map JSON (currently only supports topojson)
            hideAntarctica: true,
            borderWidth: 1,
            borderOpacity: 1,
            borderColor: '#F3B61D',
            popupTemplate: function(geography, data) {
            //this function should just return a string
              return '<div class="hoverinfo"><strong>' + geography.properties.name + '</strong></div>';
            },
            popupOnHover: true, //disable the popup while hovering
            highlightOnHover: true,
            highlightFillColor: '#F3B61D',
            highlightBorderColor: '#D90368',
            highlightBorderWidth: 2,
            highlightBorderOpacity: 1
        },
        setProjection: function(element){
          var projection = d3.geo.mercator()
            .center([lon, lat])
            .scale(200)
        },
        responsive: true,
    });
    window.map = map;
}

$(document).ready(function(){
    console.log('   _____           _ __  __                 \n' +
        '  / ____|         | |  \\/  |                \n' +
        ' | |     __ _ _ __| | \\  / | __ _ _ __  ___ \n' +
        ' | |    / _` | \'__| | |\\/| |/ _` | \'_ \\/ __|\n' +
        ' | |___| (_| | |  | | |  | | (_| | |_) \\__ \\\n' +
        '  \\_____\\__,_|_|  |_|_|  |_|\\__,_| .__/|___/\n' +
        '                                 | |        \n' +
        '                                 |_|        ');
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();
    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
    let map = new Datamap({
        element: document.getElementById('map'), fills: {
            defaultFill: '#0B5091' //the keys in this object map to the "fillKey" of [data] or [bubbles]
        },
        done: function(datamap){
            console.log(datamap);
            datamap.svg.selectAll('.datamaps-subunit').on('click',
            country_info
        )},
        geographyConfig: {
            dataUrl: null, //if not null, datamaps will fetch the map JSON (currently only supports topojson)
            hideAntarctica: true,
            borderWidth: 1,
            borderOpacity: 1,
            borderColor: '#F3B61D',
            popupTemplate: function(geography, data) {
            //this function should just return a string
              return '<div class="hoverinfo"><strong>' + geography.properties.name + '</strong></div>';
            },
            popupOnHover: true, //disable the popup while hovering
            highlightOnHover: true,
            highlightFillColor: '#F3B61D',
            highlightBorderColor: '#D90368',
            highlightBorderWidth: 2,
            highlightBorderOpacity: 1
        },
         bubblesConfig: {
            borderWidth: 2,
            borderOpacity: 1,
            borderColor: '#FFFFFF',
            popupOnHover: true,
            defaultFill: '#F3B61D',
            radius: null,
            popupTemplate: function(geography, data) {
              return '<div class="hoverinfo"><strong>' + data.name + '\n Number:' + data.weight + '</strong></div>';
            },
            fillOpacity: 0.75,
            animate: true,
            highlightOnHover: true,
            highlightFillColor: '#FC8D59',
            highlightBorderColor: 'rgba(250, 15, 160, 0.2)',
            highlightBorderWidth: 2,
            highlightBorderOpacity: 1,
            highlightFillOpacity: 0.85,
            exitDelay: 100,
            key: JSON.stringify
    },
        responsive: true,
    });
    window.map = map;
    window.render_zoom = render_zoom;
});