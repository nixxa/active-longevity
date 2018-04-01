module.exports = function (grunt) {

    // Project configuration.
    grunt.initConfig({
        uglify: {
            views: {
                files: [{
                    expand: true,
                    cwd: 'src/static/scripts/',
                    src: ['*.js'],
                    dest: 'src/static/build/',
                    ext: '.min.js',
                    extDot: 'last'
                }]
            }
        }
    });

    // Load the plugin that provides the "uglify" task.
    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Default task(s).
    grunt.registerTask('default', ['uglify']);

};