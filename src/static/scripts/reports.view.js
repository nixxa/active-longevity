/**
 * Reports view scripts
 */
define(['jquery', 'bootstrap', 'exif-reader'], function ($, bootstrap, exif) {
    'use strict';

    // render item
    function renderExifItem(img, tagName, displayName) {
        var $container = $('#image-exif');
        var tagValue = EXIF.getTag(img, tagName);
        $container.append(`<dl><dt>${ displayName ? displayName : tagName }</dt><dd>${ tagValue != undefined ? tagValue : 'N/A' }</dd></dl>`);
        return tagValue;
    }

    function formatGPSCoord(coord) {
        var result = `${coord[0]}.${coord[1]}${(coord[2] + '').replace('.','')}`;
        return result;
    }

    // image on load handler
    // https://tech.yandex.ru/maps/doc/geocoder/desc/concepts/input_params-docpage/
    function imageOnLoad() {
        if ($(this).attr('src') == '') return;
        var img = $(this)[0];
        $('#image-preview')[0].appendChild(img);
        $('#image-preview > img').attr('width', '100%');
        var $container = $('#image-exif');
        $container.html('');
        EXIF.getData(img, function() {
            renderExifItem(img, 'DateTimeOriginal', 'Дата создания');
            renderExifItem(img, 'Orientation', 'Ориентация');
            var lat = renderExifItem(img, 'GPSLatitude', 'Широта');
            var long = renderExifItem(img, 'GPSLongitude', 'Долгота');
            lat = formatGPSCoord(lat);
            long = formatGPSCoord(long);
            $.get(`https://geocode-maps.yandex.ru/1.x/?geocode=${lat},${long}&sco=latlong&format=json`, function (data) {
                if (data != undefined && data != null) {
                    var found = data.response.GeoObjectCollection.metaDataProperty.GeocoderResponseMetaData.found;
                    if (found > 0) {
                        var url = `https://yandex.ru/maps/?ll=${long}%2C${lat}&z=12`;
                        var text = data.response.GeoObjectCollection.featureMember[0].GeoObject.metaDataProperty.GeocoderMetaData.text;
                        $container.append(`<dl><dt>Адрес</dt><dd><a href="${url}" target="_blank">${text}</a></dd></dl>`);
                    }
                }
            });
        });
    }

    $(document).ready(function () {
        // on document load
        $('.js-view-photo').click(function (e) {
            $('#image-preview').html('');
            var imageSource = $(this).data('source');
            var image = new Image();
            image.onload = imageOnLoad;
            image.src = imageSource;
            $('#myModal').modal('toggle');
        });

        $('.js-selector').change(function (e) {
            var $target = $(e.target);
            var name = $target.attr('name');
            var value = $target.val();
            if (window.location.href.indexOf('?') >= 0) {
                var queryString = window.location.href.substring(window.location.href.indexOf('?')+1);
                if (queryString == '') {
                    window.location.href = `/reports/?${name}=${value}`;
                    return;
                }
                var parts = queryString.split('&');
                var result = '';
                var used = false;
                for (var i = 0; i < parts.length; i++) {
                    var pair = parts[i].split('=');
                    if (pair[0] == name) {
                        used = true;
                        if (value == 'None') {
                            continue;
                        } else {
                            result = result + `${name}=${value}` + '&';
                        }                        
                    } else {
                        result = result + parts[i] + '&';
                    }
                }
                if (!used) {
                    result = result + `${name}=${value}`;
                }
                if (result.endsWith('&')) {
                    result = result.substring(0, result.length - 1);
                }
                window.location.href = '?' + result;
            } else {
                window.location.href = `/reports/?${name}=${value}`;
            }
        });
    });
});