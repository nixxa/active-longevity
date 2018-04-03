/* RequireJS config */
require.config({
	urlArgs: 'r=v1',
	shim: {
		'bootstrap': { 'deps': ['jquery'] },
		'date-input': { 'deps': ['jquery'] },
		'dropzone': { 'deps' : ['jquery'] },
		'datatables': { 'deps': ['jquery'] }
	},
	paths: {
		'jquery': [
			'https://code.jquery.com/jquery-2.2.3.min',
			'/static/content/jquery-2.2.3/jquery.min'
		],
		'bootstrap': [
			'https://netdna.bootstrapcdn.com/bootstrap/3.3.6/js/bootstrap',
			'/static/content/bootstrap-3.3.6/js/bootstrap.min'
		],
		'moment': '/static/content/momentjs/moment-with-locales',
		'date-input': '/static/content/datetime-input/js/date-input',
		'dropzone': '/static/content/dropzonejs/dropzone',
		'audiojs': '/static/content/audiojs/audio.min',
		'datatables': '/static/content/datatables/datatables.min',
        'pica': '/static/content/pica/pica.min',
        'exifRestorer': '/static/content/exif-restorer/exifRestorer.min',
        'highcharts': [
            'https://code.highcharts.com/highcharts',
            '/static/content/highcharts-6.0.7/highcharts'
        ],
        'exif-reader': '/static/content/exif-js/exif.min',
        'checklist.view': '/static/build/checklist.view.min',
        'dashboard.view': '/static/build/dashboard.view.min'
	}
});