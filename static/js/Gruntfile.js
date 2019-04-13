var webpackConfig = require('./webpack.config.js');

module.exports = function(grunt) {

  grunt.initConfig({
    jshint: {
      files: ['Gruntfile.js', 'js/src/**/*.js'],
    },
    watch: {
      files: ['<%= jshint.files %>'],
      tasks: ['jshint']
    },
    babel: {
    options: {
      sourceMap: true,
      presets: ['@babel/preset-env']
    },
    dist: {
      files: {
        'dist/wb.js': 'dist/bundle.js'
      }
    },
  },
  uglify: {
      dist: {
        files: {
          'dist/wb.min.js': 'dist/wb.js'
        }
      }
    },
  cssmin: {
    dist: {
      files: {
        '../css/dist/wb.min.css': '../css/dist/wb.css'
      }
    }
  },
  webpack: {
      myConfig: webpackConfig,
  }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');
  grunt.loadNpmTasks('grunt-contrib-watch');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  grunt.loadNpmTasks('grunt-contrib-less');
  grunt.loadNpmTasks('grunt-contrib-cssmin');
  grunt.loadNpmTasks('grunt-babel');
  grunt.loadNpmTasks('grunt-webpack');

  grunt.registerTask('default', ['jshint', 'webpack', 'babel', 'uglify', 'cssmin']);

};