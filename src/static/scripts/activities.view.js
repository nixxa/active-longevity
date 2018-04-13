/**
 * Activities view scripts
 */
define(['jquery', 'queryString'], function ($, qs) {
    'use strict';

    return {
        initialize: function () {
            $(document).ready(function () {
                $('.js-selector').change(function (e) {
                    var $target = $(e.target);
                    var name = $target.attr('name');
                    var value = $target.val();
                    window.location.href = qs.generateQueryString(
                        window.location.href, name, value, 'activities');
                });
            });
        }
    }
});