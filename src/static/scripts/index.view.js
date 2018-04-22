/**
 * Dashboard view scripts
 */
define(['jquery'], function ($) {
    'use strict';

    $(document).ready(function () {
        $('#filter').on('keypress', function (evt) {
            var filterString = $('#filter').val();
            if (evt.key.length == 1) {
                filterString += evt.key;
            } else if (evt.key == 'Backspace') {
                filterString = filterString.substr(0, filterString.length-1);
            }
            if (filterString == '') {
                filterString = '';
                $('.js-county').show();
                $('.js-district').show();
                $('.js-district').data('hidden', false);
                return;
            }
            $('.js-district').each(function () {
                var $this = $(this);
                if ($this.data('item').toLowerCase().startsWith(filterString.toLowerCase())) {
                    $this.show();
                    $this.data('hidden', false);
                } else {
                    $this.hide();
                    $this.data('hidden', true);  
                }
                
            });
            $('.js-county').each(function () {
                var count = $(this).find('.js-district:visible').length;
                if (count == 0) {
                    $(this).hide();
                } else {
                    $(this).show();
                }
            });
        });
    });
});