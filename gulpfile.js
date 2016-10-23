var path = require('path'),
    gulp = require('gulp'),
    gutil = require('gulp-util'),
    coffee = require('gulp-coffee'),
    concat = require('gulp-concat'),

    sources,
    destinations,
    views;

sources = {
    'coffee': {
        'foodtruckservice': 'app/**/*.coffee'
    }
}

destinations = {
    'javascript': {
        'foodtruckservice': 'static/js/',
    }
}

views = {
    'partials' : 'app/views/',
    'index' : 'app/index.html'
}



// clean stream of onerror
var cleaner = function(stream) {
    stream.listeners('error').forEach(function(item) {
        if(item.name == 'onerror') this.removeListener('error', item);
    }, stream);
};

var continueOnError = function(stream) {
    return stream
        .on('pipe', function(src) {
            cleaner(src);
        })
        .on('newListener', function() {
            cleaner(this);
        });
};

gulp.task('build-foodtruckservice', function () {

    //Exlude tests from compiled dist
    return gulp.src([sources.coffee.foodtruckservice])
        .pipe(continueOnError(coffee({bare:true})).on('error', gutil.log))
        .pipe(concat('foodtruckservice.js'))
        .pipe(gulp.dest(destinations.javascript.foodtruckservice));
});

gulp.task('watcher', function () {
    gulp.watch(sources.coffee.foodtruckservice, ['build-foodtruckservice']);
    gulp.watch('app/views/**',['reload']);
    gulp.watch('app/index.html',['reload']);
})

gulp.task('build',['build-foodtruckservice']);

gulp.task('default', ['build-foodtruckservice','watcher']);
