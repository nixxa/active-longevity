/**
 * Query string parser and updater
 */
define(['jquery'], function ($) {
    return {
        generateQueryString: function (href, name, value, prefix) {
            if (href.indexOf('?') >= 0) {
                var queryString = href.substring(href.indexOf('?')+1);
                if (queryString == '') {
                    href = `/${prefix}/?${name}=${value}`;
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
                href = '?' + result;
            } else {
                href = `/${prefix}/?${name}=${value}`;
            }
            return href;
        }
    }
});