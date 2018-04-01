/***
 * Questionnaire view script.
 * Define onClick handler for question buttons.
 */
define(['require','jquery','bootstrap', 'exifRestorer'], 
    function(require, $, bootstrap, exifRestorer) {
        'use strict';

        window.restorer = exifRestorer;

        function sendFile(fileData) {
            var $form = $('#form');
            var formData = new FormData($form[0]);
            var oldfile = formData.get('photo');
            var newfile = new File([dataURItoBlob(fileData)], oldfile.name, {
                'type': oldfile.type,
            })
            formData.set('photo', newfile);

            $.ajax({
                type: 'POST',
                url: $form.attr('action'),
                data: formData,
                contentType: false,
                processData: false,
                success: function (data) {
                    if (data) {
                        window.location.href = data.url;
                    }
                },
                error: function (data) {
                    alert('There was an error uploading your file!');
                }
            });
        }

        function dataURItoBlob(dataURI) 
        {
            var binary = atob(dataURI.split(',')[1]);
            var array = [];
            for(var i = 0; i < binary.length; i++) {
                array.push(binary.charCodeAt(i));
            }
            return new Blob([new Uint8Array(array)], {type: 'image/jpeg'});
        }

        function processFile(dataURL, fileType) {
            var maxWidth = 800;
            var maxHeight = 800;
        
            var image = new Image();
            image.src = dataURL;
        
            image.onload = function () {
                var width = image.width;
                var height = image.height;
                var shouldResize = (width > maxWidth) || (height > maxHeight);
        
                if (!shouldResize) {
                    sendFile(dataURL);
                    return;
                }
        
                var newWidth;
                var newHeight;
        
                if (width > height) {
                    newHeight = height * (maxWidth / width);
                    newWidth = maxWidth;
                } else {
                    newWidth = width * (maxHeight / height);
                    newHeight = maxHeight;
                }
        
                var canvas = document.createElement('canvas');
        
                canvas.width = newWidth;
                canvas.height = newHeight;
        
                var context = canvas.getContext('2d');
        
                context.drawImage(this, 0, 0, newWidth, newHeight);
        
                var resizedDataURL = canvas.toDataURL(fileType);
                resizedDataURL = 'data:image/jpeg;base64,' +
                    window.restorer.restore(dataURL, resizedDataURL);
        
                sendFile(resizedDataURL);
            };
        
            image.onerror = function () {
                alert('There was an error processing your file!');
            };
        }

        function readFile(file) {
            var reader = new FileReader();
        
            reader.onloadend = function (evt) {
                processFile(reader.result, file.type);
            }
        
            reader.onerror = function () {
                alert('There was an error reading the file!');
            }
        
            reader.readAsDataURL(file);
        }

        // document.onload
        $(function () {
            var $inputField = $('#photo');

            var $executor = $('#executor');
            var $activity = $('#activity');

            $executor.on('change', function (e) {
                if ($executor.val() == '') return;
                $activity.html('');
                var items = window.data[$executor.val()];
                if (items.length > 1) {
                    $activity.append($('<option>', {
                        value: '',
                        text: '[ ... выберите из списка ... ]'
                    }));
                }
                for (var key in items) {
                    $activity.append($('<option>', {
                        value: items[key],
                        text: items[key]
                    }));
                }
            });
            for (var key in window.data) {
                $executor.append($('<option>', {
                    value: key,
                    text: key
                }));
            };

            $('#form-save').on('click', function (e) {
                var file = $inputField[0].files[0];
        
                if (file) {
                    if (/^image\//i.test(file.type)) {
                        readFile(file);
                    } else {
                        alert('Not a valid image!');
                    }
                }
            });
        });
    }
);