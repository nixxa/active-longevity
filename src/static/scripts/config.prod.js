/* RequireJS config */
require.config({
	urlArgs: 'r=v1',
	shim: {
		'bootstrap': { 'deps': ['jquery'] },
        'select2': { 'deps': ['jquery'] }
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
        'exifRestorer': '/static/content/exif-restorer/exifRestorer.min',
        'highcharts': [
            'https://code.highcharts.com/highcharts',
            '/static/content/highcharts-6.0.7/highcharts'
        ],
        'select2': '/static/content/select2-4.0.5/js/select2.min',
        'exif-reader': '/static/content/exif-js/exif.min',
        'queryString': '/static/build/queryString.min',
        'checklist.view': '/static/build/checklist.view.min',
        'dashboard.view': '/static/build/dashboard.view.min',
        'reports.view': '/static/build/reports.view.min',
        'activities.view': '/static/build/activities.view.min',
        'index.view': '/static/build/index.view.min'
	}
});