module.exports = function(grunt) {
  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    browserify: {
      options: {
        transform: [
          ['babelify']
        ],
        browserifyOptions: {
          debug: true
        }
      },
      build: {
        src: './index.js',
        dest: './build/bundle.js'
      }
    }
  });

  grunt.loadNpmTasks('grunt-browserify');
}
