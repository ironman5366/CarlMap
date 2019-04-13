import '../node_modules/bootstrap/dist/js/bootstrap.min.js';
import $ from '../node_modules/jquery/dist/jquery.slim.min.js';
import '../../css/sass/main.scss';
import '../../css/less/styles.less';


$(document).ready(function(){
    console.log('   _____           _ __  __                 \n' +
        '  / ____|         | |  \\/  |                \n' +
        ' | |     __ _ _ __| | \\  / | __ _ _ __  ___ \n' +
        ' | |    / _` | \'__| | |\\/| |/ _` | \'_ \\/ __|\n' +
        ' | |___| (_| | |  | | |  | | (_| | |_) \\__ \\\n' +
        '  \\_____\\__,_|_|  |_|_|  |_|\\__,_| .__/|___/\n' +
        '                                 | |        \n' +
        '                                 |_|        ');

    let map = new Datamap({
        element: document.getElementById('map'), fills: {
            defaultFill: '#0B5091' //the keys in this object map to the "fillKey" of [data] or [bubbles]
        },
        geographyConfig: {
            dataUrl: nulil, //if not null, datamaps will fetch the map JSON (currently only supports topojson)
            hideAntarctica: true,
            borderWidth: 1,
            borderOpacity: 1,
            borderColor: '#F3B61D',
            popupTemplate: function(geography, data) { //this function should just return a string
              return '<div class="hoverinfo"><strong>' + geography.properties.name + '</strong></div>';
            },
            popupOnHover: true, //disable the popup while hovering
            highlightOnHover: true,
            highlightFillColor: '#F3B61D',
            highlightBorderColor: '#D90368',
            highlightBorderWidth: 2,
            highlightBorderOpacity: 1
        },
        responsive: true,
    });
});